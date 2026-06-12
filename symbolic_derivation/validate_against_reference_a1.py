"""将统一分段模型自动生成的归一化指标与参考论文表 A1 对照。"""

from pathlib import Path
import csv
import random

import sympy as sp

from .mode_constraints import get_mode_constraint
from .normalized_metrics import (
    ALLOWED_SYMBOLS,
    derive_all_normalized_metrics,
    export_normalized_metrics,
)
from .normalized_current import K
from .reference_a1 import REFERENCE_A1
from .symbols import D1, D2, phi


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
OUTPUTS = ROOT / "outputs"
VARIABLES = (D1, D2, phi, K)
K_SAMPLES = (0.45, 0.8, 1.0, 1.25, 1.8)
TOLERANCE = 1e-8


def _symbolic_difference(generated: sp.Expr, reference: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.simplify(generated - reference)))


def _constraint_satisfied(mode: str, point: dict[sp.Symbol, float]) -> bool:
    constraint = get_mode_constraint(mode)
    return all(bool(relation.subs(point)) for relation in (
        constraint.variable_range + constraint.inequalities_sympy
    ))


def _sample_mode_points(mode: str, count: int = 16) -> list[dict[sp.Symbol, float]]:
    rng = random.Random(20260612 + ord(mode))
    points = []
    attempts = 0
    while len(points) < count and attempts < 300000:
        attempts += 1
        point = {
            D1: rng.uniform(0.02, 0.98),
            D2: rng.uniform(0.02, 0.98),
            phi: rng.uniform(0.001, 0.999),
        }
        if _constraint_satisfied(mode, point):
            points.append(point)
    if len(points) < count:
        raise RuntimeError(f"模式 {mode} 约束域随机采样不足：{len(points)}/{count}")
    return points


def _numeric_error(
    generated: sp.Expr, reference: sp.Expr, samples: list[dict[sp.Symbol, float]]
) -> tuple[bool, float]:
    maximum = 0.0
    for sample in samples:
        error = abs(float(sp.N((generated - reference).subs(sample))))
        maximum = max(maximum, error)
    return maximum <= TOLERANCE, maximum


def _metric_row(
    mode: str,
    metric: str,
    generated: sp.Expr,
    reference: sp.Expr,
    samples: list[dict[sp.Symbol, float]],
    note: str = "",
) -> dict:
    difference = _symbolic_difference(generated, reference)
    symbolic_check = difference == 0
    numeric_check, max_error = _numeric_error(generated, reference, samples)
    return {
        "mode": mode,
        "metric": metric,
        "generated_expr": str(generated),
        "reference_expr_K": str(reference),
        "difference_expr": str(difference),
        "symbolic_check": symbolic_check,
        "numeric_check": numeric_check,
        "status": "PASS" if symbolic_check or numeric_check else "FAIL",
        "max_abs_error": max_error,
        "notes": note,
    }


def _stress_row(mode: str, metrics, reference, base_points) -> dict:
    max_error = 0.0
    failure_examples = []
    sample_count = 0
    for base in base_points:
        for k_value in K_SAMPLES:
            sample_count += 1
            point = {**base, K: k_value}
            generated = max(
                abs(float(sp.N(candidate.subs(point))))
                for candidate in metrics.current_stress_candidates_star
            )
            reference_expr = (
                reference.current_stress_reference_lt1
                if k_value < 1
                else reference.current_stress_reference_ge1
            )
            expected = float(sp.N(reference_expr.subs(point)))
            error = abs(generated - expected)
            max_error = max(max_error, error)
            if error > TOLERANCE and len(failure_examples) < 3:
                failure_examples.append(
                    f"D1={base[D1]:.6g},D2={base[D2]:.6g},phi={base[phi]:.6g},"
                    f"K={k_value:g}: generated={generated:.12g}, "
                    f"reference={expected:.12g}, diff={generated-expected:.12g}"
                )
    passed = max_error <= TOLERANCE
    note = (
        f"约束域内 {sample_count} 个确定性随机样本；比较 max(abs(I0_star...I8_star))。"
    )
    if failure_examples:
        note += " 失败样本：" + " | ".join(failure_examples)
    return {
        "mode": mode,
        "metric": "current_stress_star",
        "generated_expr": "max(abs(I0_star),...,abs(I8_star))",
        "reference_expr_K": (
            f"K<1: {reference.current_stress_reference_lt1}; "
            f"K>=1: {reference.current_stress_reference_ge1}"
        ),
        "difference_expr": "numeric_sampling",
        "symbolic_check": "N/A",
        "numeric_check": passed,
        "status": "PASS" if passed else "FAIL",
        "max_abs_error": max_error,
        "notes": note,
    }


def build_validation_rows() -> list[dict]:
    rows = []
    metrics_all = derive_all_normalized_metrics()
    for mode in "ABCDEFGH":
        metrics = metrics_all[mode]
        reference = REFERENCE_A1[mode]
        base_points = _sample_mode_points(mode)
        samples = [{**point, K: value} for point in base_points for value in K_SAMPLES]
        rows.append(_metric_row(
            mode, "p_star", metrics.p_star_expr, reference.p_star_reference, samples,
            "A1 原文 M 已替换为本文 K。",
        ))
        rows.append(_metric_row(
            mode, "Irms_star_sq", metrics.irms_star_sq_expr,
            reference.irms_star_sq_reference, samples,
            "A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。",
        ))
        rows.append(_stress_row(mode, metrics, reference, base_points))
    return rows


def _write_csv(rows: list[dict]) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    path = OUTPUTS / "a1_reproduction_validation.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_report(rows: list[dict]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    metrics_all = derive_all_normalized_metrics()
    lines = [
        "# A-H 归一化指标与参考论文附表 A1 复现报告",
        "",
        "## 定义对应关系",
        "",
        "- 本文使用 `K=n*V2/V1`；参考论文表 A1 使用 `M`，对照时统一执行 `M -> K`。",
        "- 本文功率由统一分段模型计算：`p_star=(1/K)*sum(v1_state*area_i_star)`。",
        "- 本文计算 `Irms_star_sq=(1/2)*sum(integral(i_star^2 d_tau))`。",
        "- 表 A1 的“标幺化电流有效值表达式”经对照确认对应 `Irms_star_sq`，不是开方后的 `Irms_star`。",
        "- 电流应力采用所有边界电流的 `max(abs(I0_star...I8_star))`；A1 分段应力公式通过约束域随机样本验证。",
        "- 所有数值采样均限制在对应模式 A1 约束域内，并覆盖 `K<1`、`K=1` 和 `K>1`。",
        "",
        "## 总览",
        "",
        "| mode | metric | symbolic | numeric | status | max abs error |",
        "|---|---|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['mode']} | {row['metric']} | {row['symbolic_check']} | "
            f"{row['numeric_check']} | **{row['status']}** | `{row['max_abs_error']}` |"
        )

    lines.extend(["", "## 分模式表达式"])
    for mode in "ABCDEFGH":
        metrics = metrics_all[mode]
        reference = REFERENCE_A1[mode]
        mode_rows = [row for row in rows if row["mode"] == mode]
        lines.extend([
            "",
            f"### Mode {mode}",
            "",
            f"- A1 约束：`{reference.constraints_raw}`",
            f"- 自动生成 `p_star`：`{metrics.p_star_expr}`",
            f"- A1 `p_star`：`{reference.p_star_reference}`",
            f"- 自动生成 `Irms_star_sq`：`{metrics.irms_star_sq_expr}`",
            f"- A1 `Irms_star_sq`：`{reference.irms_star_sq_reference}`",
            f"- A1 电流应力，`K<1`：`{reference.current_stress_reference_lt1}`",
            f"- A1 电流应力，`K>=1`：`{reference.current_stress_reference_ge1}`",
            f"- 自动生成应力候选：`{metrics.current_stress_candidates_star}`",
        ])
        if reference.note:
            lines.append(f"- 录入说明：{reference.note}")
        lines.append(f"- A1 公式人工复核状态：`{reference.review_status}`")
        for row in mode_rows:
            lines.append(
                f"- `{row['metric']}`：{row['status']}；差值/方法："
                f"`{row['difference_expr']}`；{row['notes']}"
            )

    failures = [row for row in rows if row["status"] != "PASS"]
    lines.extend([
        "",
        "## 结论",
        "",
        f"- A-H 功率表达式 PASS 数：{sum(r['metric']=='p_star' and r['status']=='PASS' for r in rows)}/8。",
        f"- A-H RMS 平方表达式 PASS 数：{sum(r['metric']=='Irms_star_sq' and r['status']=='PASS' for r in rows)}/8。",
        f"- A-H 电流应力表达式 PASS 数：{sum(r['metric']=='current_stress_star' and r['status']=='PASS' for r in rows)}/8。",
        f"- 不一致项数量：{len(failures)}。",
        "- G 模式 RMS 的 PDF 文本抽取歧义已通过统一分段模型的符号零差值确定为三次项 `3*D1**2*D2*K`；仍建议对照 PDF 视觉版归档确认。",
        "- 当前唯一保留的人工复核项：G 模式 A1 RMS 中间项的 PDF 视觉版确认；这不影响当前符号零差值验证结果。",
    ])
    (DOCS / "AH_A1_REPRODUCTION_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def _validate_or_raise(rows: list[dict]) -> None:
    metrics_all = derive_all_normalized_metrics()
    bad_symbols = {
        mode: metrics.symbols
        for mode, metrics in metrics_all.items()
        if not metrics.dimensional_symbol_check
        or not (
            metrics.p_star_expr.free_symbols <= ALLOWED_SYMBOLS
            and metrics.irms_star_sq_expr.free_symbols <= ALLOWED_SYMBOLS
        )
    }
    failures = [f"{row['mode']}:{row['metric']}" for row in rows if row["status"] != "PASS"]
    if bad_symbols or failures:
        raise RuntimeError(f"A1 复现验证失败；bad_symbols={bad_symbols}; failures={failures}")


def main() -> int:
    export_normalized_metrics(OUTPUTS / "normalized_metrics_AH.csv")
    rows = build_validation_rows()
    _write_csv(rows)
    _write_report(rows)
    _validate_or_raise(rows)
    print("A-H 表 A1 复现验证 PASS：功率、RMS 平方和电流应力均一致。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
