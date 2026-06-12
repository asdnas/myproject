"""基于 VoltageSegment 的符号电流递推与梯形面积约束求解。"""

import csv
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

from .symbols import D1, D2, I0, L, Th, Ts, V1, V2, n, phi
from .voltage_segments import get_voltage_segments


@dataclass(frozen=True)
class CurrentSolution:
    i0_expr: sp.Expr
    currents: tuple[sp.Expr, ...]
    areas: tuple[sp.Expr, ...]
    currents_raw: tuple[sp.Expr, ...]
    total_area_raw: sp.Expr
    area_constraint_after_substitution: sp.Expr
    total_time_expr: sp.Expr
    total_time_minus_ts: sp.Expr
    sum_delta_i_expr: sp.Expr
    i8_minus_i0: sp.Expr
    solve_status: str = "success"


def solve_currents(segments: list) -> CurrentSolution:
    currents_raw = [I0]
    for segment in segments:
        currents_raw.append(
            sp.simplify(currents_raw[-1] + segment.slope_expr * segment.duration_expr)
        )
    areas_raw = tuple(
        sp.simplify((currents_raw[i] + currents_raw[i + 1]) * segment.duration_expr / 2)
        for i, segment in enumerate(segments)
    )
    total_area = sp.simplify(sum(areas_raw))
    solutions = sp.solve(total_area, I0)
    if not solutions:
        raise RuntimeError("面积约束无法求解 I0。")
    i0_expr = sp.simplify(solutions[0])
    currents = tuple(sp.simplify(value.subs(I0, i0_expr)) for value in currents_raw)
    areas = tuple(sp.simplify(value.subs(I0, i0_expr)) for value in areas_raw)
    total_time = sp.simplify(sum(segment.duration_expr for segment in segments))
    sum_delta_i = sp.simplify(sum(
        segment.slope_expr * segment.duration_expr for segment in segments
    ))
    return CurrentSolution(
        i0_expr=i0_expr,
        currents=currents,
        areas=areas,
        currents_raw=tuple(currents_raw),
        total_area_raw=total_area,
        area_constraint_after_substitution=sp.simplify(total_area.subs(I0, i0_expr)),
        total_time_expr=total_time,
        total_time_minus_ts=sp.simplify(total_time - Ts),
        sum_delta_i_expr=sum_delta_i,
        i8_minus_i0=sp.simplify(currents[-1] - currents[0]),
    )


def derive_mode_currents(mode_label: str) -> CurrentSolution:
    return solve_currents(get_voltage_segments(mode_label))


def derive_all_mode_currents() -> dict[str, CurrentSolution]:
    results = {}
    for mode in "ABCDEFGH":
        try:
            results[mode] = derive_mode_currents(mode)
        except Exception as exc:
            raise RuntimeError(f"模式 {mode} 电流符号推导失败: {exc}") from exc
    return results


def export_mode_current_csvs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    results = derive_all_mode_currents()
    current_rows = []
    area_rows = []
    check_rows = []
    for mode, solution in results.items():
        for index, current in enumerate(solution.currents):
            current_rows.append({
                "mode": mode,
                "current_index": index,
                "current_name": f"I{index}",
                "current_expr": str(current),
                "current_latex": sp.latex(current),
            })
        for index, area in enumerate(solution.areas, start=1):
            area_rows.append({
                "mode": mode,
                "segment_index": index,
                "area_expr": str(area),
                "area_latex": sp.latex(area),
            })
        check_rows.append({
            "mode": mode,
            "total_time_expr": str(solution.total_time_expr),
            "total_time_minus_Ts": str(solution.total_time_minus_ts),
            "sum_delta_i_expr": str(solution.sum_delta_i_expr),
            "I8_minus_I0": str(solution.i8_minus_i0),
            "area_constraint_expr": str(solution.total_area_raw),
            "area_after_substitution": str(solution.area_constraint_after_substitution),
            "solve_status": solution.solve_status,
            "notes": "VoltageEdge 边界电流；尚未映射具体开关事件。",
        })
    _write_csv(output_dir / "mode_currents_symbolic.csv", current_rows)
    _write_csv(output_dir / "mode_segment_areas_symbolic.csv", area_rows)
    _write_csv(output_dir / "mode_current_checks.csv", check_rows)


def segments_from_legacy_config(config: dict) -> list:
    """适配 legacy 配置；保持 legacy 的加号斜率约定用于精确对照。"""
    from .segment_builder import Segment
    result = []
    for index, item in enumerate(config["segments"], start=1):
        c1, c2, c3, c0 = item["time"]
        duration = sp.simplify((c1 * D1 + c2 * D2 + c3 * phi + c0) * Th)
        v_l = sp.simplify(item["v1"] * V1 + item["v2"] * n * V2)
        result.append(
            Segment(index, f"legacy_boundary_{index - 1}", f"legacy_boundary_{index}",
                    sp.Integer(0), sp.Integer(0), duration, item["v1"], item["v2"],
                    v_l, sp.simplify(v_l / L), note="来自 config.py；采用 legacy 加号约定。")
        )
    return result


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    output_dir = Path(__file__).resolve().parent / "outputs"
    export_mode_current_csvs(output_dir)
    print(f"已导出 A-H 电流结果到 {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
