"""验证并导出 A-H 八模态归一化电流结果。"""

from pathlib import Path
import csv

import sympy as sp

from .current_solver import derive_all_mode_currents
from .legacy_current_compare import compare_all_legacy_currents
from .normalized_current import (
    Ib,
    K,
    Ths,
    derive_all_normalized_currents,
    dimensional_to_normalized,
    export_normalized_csvs,
)
from .symbols import L, Ts, V1, V2, fs, n


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
OUTPUTS = ROOT / "outputs"


def _zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def build_validation_rows() -> list[dict]:
    normalized = derive_all_normalized_currents()
    dimensional = derive_all_mode_currents()
    legacy = compare_all_legacy_currents()
    rows = []
    for mode in "ABCDEFGH":
        solution = normalized[mode]
        differences = tuple(
            sp.factor(sp.simplify(
                current_star - dimensional_to_normalized(current_dimensional)
            ))
            for current_star, current_dimensional in zip(
                solution.currents_star, dimensional[mode].currents
            )
        )
        rows.append({
            "mode": mode,
            "sum_tau_expr": str(solution.sum_tau_expr),
            "sum_tau_minus_2": str(solution.sum_tau_minus_two),
            "sum_delta_I_star": str(solution.sum_delta_i_star_expr),
            "I8_star_minus_I0_star": str(solution.i8_star_minus_i0_star),
            "normalized_average_area_after_I0": str(
                solution.normalized_area_after_substitution
            ),
            "all_dimensional_edges_consistent": all(_zero(value) for value in differences),
            "dimensional_difference_list": str(differences),
            "legacy_dimensional_consistency": (
                legacy[mode].all_equal if mode in legacy else "N/A"
            ),
            "solve_status": solution.solve_status,
            "notes": "纯符号验证；未使用数值采样。",
        })
    return rows


def write_validation_csv(rows: list[dict]) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    path = OUTPUTS / "normalized_current_validation_AH.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    normalized = derive_all_normalized_currents()
    legacy = compare_all_legacy_currents()
    lines = [
        "# A-H 八模态归一化分段电流",
        "",
        "## 归一化定义",
        "",
        "- 本文使用 `K = n*V2/V1` 表示电压变比；不在新模块中使用参考文献常见的 `M`，以避免与本文符号体系混淆。",
        "- `Ts = 1/fs`，`Ths = Ts/2`。",
        "- `Ib = V1/(4*fs*L) = V1*Ts/(4*L)`。",
        "- `Pb = n*V1*V2/(8*fs*L)`；`p_star` 已在 `normalized_metrics.py` 中实现并与表 A1 对照。",
        "- `tau_k = duration_k/Ths`，完整周期满足 `sum(tau_k)=2`。",
        "- `vL_star_k = v1_state_k - K*v2_state_k`。",
        "- `delta_I_star_k = 2*vL_star_k*tau_k`。",
        "- `I_(k+1)_star = I_k_star + delta_I_star_k`。",
        "- 零平均电流约束：`sum((I_k_star + I_(k+1)_star)*tau_k/2)=0`。",
        "",
        "## 总体验证",
        "",
        "| mode | sum(tau) | sum(tau)-2 | sum(delta I*) | I8*-I0* | normalized area | I/Ib consistency |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['mode']} | `{row['sum_tau_expr']}` | `{row['sum_tau_minus_2']}` | "
            f"`{row['sum_delta_I_star']}` | `{row['I8_star_minus_I0_star']}` | "
            f"`{row['normalized_average_area_after_I0']}` | "
            f"{row['all_dimensional_edges_consistent']} |"
        )
    lines.extend([
        "",
        "## D/G Legacy 与已有结果",
        "",
        f"- D 模式已有有量纲结果与 legacy 周期对齐后逐项一致：`{legacy['D'].all_equal}`。",
        f"- G 模式已有有量纲结果与 legacy 周期对齐后逐项一致：`{legacy['G'].all_equal}`。",
        "- 本次直接无量纲递推又与已有有量纲结果除以 `Ib` 后逐项一致，因此 D/G 归一化结果间接通过 legacy 回归验证。",
    ])

    for mode in "ABCDEFGH":
        solution = normalized[mode]
        lines.extend([
            "",
            f"## Mode {mode}",
            "",
            f"- `I0_star = {sp.factor(solution.i0_star_expr)}`",
            f"- LaTeX: `${sp.latex(sp.factor(solution.i0_star_expr))}$`",
            "",
            "### 归一化分段",
            "",
            "| segment | tau | v1 | v2 | vL_star | delta_I_star |",
            "|---:|---|---:|---:|---|---|",
        ])
        for segment in solution.segments:
            lines.append(
                f"| {segment.index} | `{segment.tau_expr}` | {segment.v1_state} | "
                f"{segment.v2_state} | `{segment.vL_star_expr}` | "
                f"`{segment.delta_i_star_expr}` |"
            )
        lines.extend([
            "",
            "### 归一化边界电流",
            "",
            "| edge | plain expression | LaTeX |",
            "|---:|---|---|",
        ])
        for index, current in enumerate(solution.currents_star):
            lines.append(
                f"| I{index}_star | `{sp.factor(current)}` | "
                f"`${sp.latex(sp.factor(current))}$` |"
            )

    lines.extend([
        "",
        "## 后续归一化指标",
        "",
        f"- 已定义 `Pb = n*V1*V2/(8*fs*L)`。",
        "- `derive_normalized_power(mode)` 已委托到 `normalized_metrics.py` 的统一实现。",
        "- `p_star`、`Irms_star_sq` 与电流应力的表 A1 对照结果见 `AH_A1_REPRODUCTION_REPORT.md`。",
    ])
    (DOCS / "AH_NORMALIZED_CURRENT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def validate_or_raise(rows: list[dict]) -> None:
    failures = []
    for row in rows:
        if row["sum_tau_minus_2"] != "0":
            failures.append(f"{row['mode']}: sum(tau)-2 != 0")
        if row["sum_delta_I_star"] != "0":
            failures.append(f"{row['mode']}: sum(delta I*) != 0")
        if row["I8_star_minus_I0_star"] != "0":
            failures.append(f"{row['mode']}: I8*-I0* != 0")
        if row["normalized_average_area_after_I0"] != "0":
            failures.append(f"{row['mode']}: normalized average current != 0")
        if not row["all_dimensional_edges_consistent"]:
            failures.append(f"{row['mode']}: I*/(I/Ib) mismatch")
        if row["mode"] in {"D", "G"} and not row["legacy_dimensional_consistency"]:
            failures.append(f"{row['mode']}: existing dimensional result/legacy mismatch")
    if failures:
        raise RuntimeError("归一化电流验证失败：" + "; ".join(failures))


def main() -> int:
    # 显式检查基础定义，防止后续符号定义被意外修改。
    assert sp.simplify(Ths - Ts / 2) == 0
    assert sp.simplify(Ib - V1 / (4 * fs * L)) == 0

    export_normalized_csvs(OUTPUTS)
    rows = build_validation_rows()
    write_validation_csv(rows)
    write_markdown(rows)
    validate_or_raise(rows)
    print("A-H 归一化电流验证 PASS：sum(tau)=2，周期闭合，零平均，且与 I/Ib 逐项一致。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
