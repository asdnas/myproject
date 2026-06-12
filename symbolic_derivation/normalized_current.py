"""A-H 八模态分段电流的直接无量纲推导。

本模块只读取已验证的 VoltageSegment，不修改原分段。归一化定义为：
    K = n*V2/V1
    Ths = Ts/2
    Ib = V1/(4*fs*L)
    tau = duration/Ths
    vL_star = v1_state - K*v2_state
    delta_I_star = 2*vL_star*tau
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import csv

import sympy as sp

from .symbols import L, Th, Ts, V1, fs
from .voltage_segments import get_voltage_segments


K = sp.symbols("K", positive=True, real=True)
I0_star_symbol = sp.symbols("I0_star", real=True)
Ths = Th
Ib = V1 / (4 * fs * L)


@dataclass(frozen=True)
class NormalizedSegment:
    index: int
    tau_expr: sp.Expr
    v1_state: int
    v2_state: int
    vL_star_expr: sp.Expr
    delta_i_star_expr: sp.Expr
    i_start_star: sp.Expr
    i_end_star: sp.Expr
    zero_duration_possible: bool


@dataclass(frozen=True)
class NormalizedCurrentSolution:
    mode: str
    i0_star_expr: sp.Expr
    currents_star: tuple[sp.Expr, ...]
    currents_star_raw: tuple[sp.Expr, ...]
    segments: tuple[NormalizedSegment, ...]
    normalized_areas: tuple[sp.Expr, ...]
    normalized_area_raw: sp.Expr
    normalized_area_after_substitution: sp.Expr
    sum_tau_expr: sp.Expr
    sum_tau_minus_two: sp.Expr
    sum_delta_i_star_expr: sp.Expr
    i8_star_minus_i0_star: sp.Expr
    solve_status: str = "success"


def _clean(expr: sp.Expr) -> sp.Expr:
    """适度化简，避免对较长表达式进行高成本全展开。"""
    return sp.factor(sp.simplify(expr))


@lru_cache(maxsize=8)
def derive_normalized_current(mode_label: str) -> NormalizedCurrentSolution:
    mode = mode_label.upper()
    voltage_segments = get_voltage_segments(mode)

    tau_values = tuple(_clean(segment.duration_expr / Ths) for segment in voltage_segments)
    v_l_star_values = tuple(
        _clean(segment.v1_state - K * segment.v2_state)
        for segment in voltage_segments
    )
    delta_values = tuple(
        _clean(2 * v_l_star * tau)
        for v_l_star, tau in zip(v_l_star_values, tau_values)
    )

    currents_raw = [I0_star_symbol]
    for delta in delta_values:
        currents_raw.append(_clean(currents_raw[-1] + delta))

    areas_raw = tuple(
        _clean((currents_raw[index] + currents_raw[index + 1]) * tau / 2)
        for index, tau in enumerate(tau_values)
    )
    total_area_raw = _clean(sum(areas_raw))
    solutions = sp.solve(total_area_raw, I0_star_symbol)
    if not solutions:
        raise RuntimeError(f"模式 {mode} 的归一化面积约束无法求解 I0_star")

    i0_star = _clean(solutions[0])
    currents = tuple(_clean(value.subs(I0_star_symbol, i0_star)) for value in currents_raw)
    areas = tuple(_clean(value.subs(I0_star_symbol, i0_star)) for value in areas_raw)

    normalized_segments = tuple(
        NormalizedSegment(
            index=segment.index,
            tau_expr=tau_values[index],
            v1_state=segment.v1_state,
            v2_state=segment.v2_state,
            vL_star_expr=v_l_star_values[index],
            delta_i_star_expr=delta_values[index],
            i_start_star=currents[index],
            i_end_star=currents[index + 1],
            zero_duration_possible=segment.zero_duration_possible,
        )
        for index, segment in enumerate(voltage_segments)
    )

    sum_tau = _clean(sum(tau_values))
    sum_delta = _clean(sum(delta_values))
    return NormalizedCurrentSolution(
        mode=mode,
        i0_star_expr=i0_star,
        currents_star=currents,
        currents_star_raw=tuple(currents_raw),
        segments=normalized_segments,
        normalized_areas=areas,
        normalized_area_raw=total_area_raw,
        normalized_area_after_substitution=_clean(
            total_area_raw.subs(I0_star_symbol, i0_star)
        ),
        sum_tau_expr=sum_tau,
        sum_tau_minus_two=_clean(sum_tau - 2),
        sum_delta_i_star_expr=sum_delta,
        i8_star_minus_i0_star=_clean(currents[-1] - currents[0]),
    )


def derive_all_normalized_currents() -> dict[str, NormalizedCurrentSolution]:
    return {mode: derive_normalized_current(mode) for mode in "ABCDEFGH"}


def derive_normalized_power(mode_label: str):
    """兼容入口；实际实现位于 normalized_metrics，避免在本模块重复公式。"""
    from .normalized_metrics import derive_normalized_power as derive

    return derive(mode_label)


def export_normalized_csvs(output_dir: Path) -> None:
    from .current_solver import derive_all_mode_currents

    output_dir.mkdir(parents=True, exist_ok=True)
    normalized = derive_all_normalized_currents()
    dimensional = derive_all_mode_currents()
    edge_rows = []
    segment_rows = []

    for mode in "ABCDEFGH":
        solution = normalized[mode]
        dimensional_solution = dimensional[mode]
        for index, current_star in enumerate(solution.currents_star):
            dimensional_as_star = dimensional_to_normalized(
                dimensional_solution.currents[index]
            )
            edge_rows.append({
                "mode": mode,
                "edge_index": index,
                "I_star_expr": str(current_star),
                "I_star_latex": sp.latex(current_star),
                "I_dimensional_expr_if_available": str(
                    dimensional_solution.currents[index]
                ),
                "check_dimensional_consistency": _clean(
                    current_star - dimensional_as_star
                ) == 0,
                "notes": "直接无量纲递推；边界顺序与既有 VoltageEdge 保持一致。",
            })
        for segment in solution.segments:
            segment_rows.append({
                "mode": mode,
                "segment_index": segment.index,
                "tau_expr": str(segment.tau_expr),
                "v1_state": segment.v1_state,
                "v2_state": segment.v2_state,
                "vL_star_expr": str(segment.vL_star_expr),
                "delta_I_star_expr": str(segment.delta_i_star_expr),
                "I_start_star": str(segment.i_start_star),
                "I_end_star": str(segment.i_end_star),
                "zero_duration_possible": segment.zero_duration_possible,
            })

    _write_csv(output_dir / "normalized_current_edges_AH.csv", edge_rows)
    _write_csv(output_dir / "normalized_segments_AH.csv", segment_rows)


def dimensional_to_normalized(current_expr: sp.Expr) -> sp.Expr:
    """将已有有量纲电流除以 Ib，并用 V2=K*V1/n 转为 K 表达式。"""
    from .symbols import V2, n

    return _clean((current_expr / Ib).subs(V2, K * V1 / n))


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    output_dir = Path(__file__).resolve().parent / "outputs"
    export_normalized_csvs(output_dir)
    print(f"已导出 A-H 归一化电流与分段 CSV：{output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
