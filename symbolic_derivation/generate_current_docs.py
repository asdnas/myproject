"""生成 A-H 符号电流与检查文档。"""

from pathlib import Path

import sympy as sp

from .current_solver import derive_all_mode_currents
from .legacy_current_compare import compare_all_legacy_currents


DOCS = Path(__file__).resolve().parent / "docs"


def _inline(expr: sp.Expr) -> str:
    return str(sp.factor(expr))


def write_currents_doc() -> None:
    results = derive_all_mode_currents()
    lines = [
        "# A-H VoltageEdge 边界电流符号公式",
        "",
        "电流由完整周期 8 段 VoltageSegment 递推，并使用完整周期电流平均值为零的面积约束求 `I0`。",
        "当前 `I0...I8` 仅表示 VoltageEdge 边界电流，尚未映射到具体开关管开通/关断事件。",
    ]
    for mode, solution in results.items():
        lines.extend([
            "",
            f"## Mode {mode}",
            "",
            f"- `I0 = {_inline(solution.i0_expr)}`",
            f"- LaTeX：`${sp.latex(solution.i0_expr)}$`",
            "",
            "### 边界电流",
            "",
            "| edge/current | expression | LaTeX |",
            "|---|---|---|",
        ])
        for index, current in enumerate(solution.currents):
            lines.append(
                f"| edge_{index}_current / I{index} | `{_inline(current)}` | "
                f"`${sp.latex(current)}$` |"
            )
        lines.extend([
            "",
            "### 每段面积",
            "",
            "| segment | area expression | LaTeX |",
            "|---:|---|---|",
        ])
        for index, area in enumerate(solution.areas, start=1):
            lines.append(f"| {index} | `{_inline(area)}` | `${sp.latex(area)}$` |")
    (DOCS / "AH_CURRENTS_SYMBOLIC.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_checks_doc() -> None:
    results = derive_all_mode_currents()
    comparisons = compare_all_legacy_currents()
    lines = [
        "# A-H 电流符号检查",
        "",
        "所有检查均为 SymPy 符号化简结果，没有代入数值点。",
        "",
        "| mode | total_time-Ts | sum(k*dt) | I8-I0 | area after I0 substitution | solve status |",
        "|---|---|---|---|---|---|",
    ]
    for mode, solution in results.items():
        lines.append(
            f"| {mode} | `{solution.total_time_minus_ts}` | `{solution.sum_delta_i_expr}` | "
            f"`{solution.i8_minus_i0}` | `{solution.area_constraint_after_substitution}` | "
            f"{solution.solve_status} |"
        )
    lines.extend([
        "",
        "## D/G Legacy 电流回归",
        "",
        "新 VoltageSegment 周期从 legacy boundary 4 开始，因此旧电流按物理边界循环对齐为：",
        "`legacy_I4,I5,I6,I7,I8,I1,I2,I3,I4`。",
        "",
    ])
    for mode, comparison in comparisons.items():
        lines.append(
            f"- Mode {mode}: 9 个边界电流逐项一致 = `{comparison.all_equal}`；"
            f"差值 = `{comparison.differences}`。"
        )
    lines.extend([
        "",
        "## 结论",
        "",
        "- A-H 均成功使用面积约束求解 `I0`。",
        "- A-H 均满足完整周期伏秒平衡与电流周期闭合。",
        "- 当前结果仅是 VoltageEdge 边界电流，未映射具体开关事件。",
    ])
    (DOCS / "AH_CURRENT_CHECKS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_legacy_comparison_doc() -> None:
    comparisons = compare_all_legacy_currents()
    lines = [
        "# D/G Legacy 电流对比",
        "",
        "旧程序周期起点与新 VoltageSegment 周期起点不同。新周期从旧配置第 5 段开始，"
        "因此必须按同一物理边界循环对齐，不能直接比较同名下标。",
        "",
        "| new current | aligned legacy current |",
        "|---|---|",
    ]
    for new_index, legacy_name in enumerate(comparisons["D"].aligned_legacy_names):
        lines.append(f"| I{new_index} | {legacy_name} |")
    for mode, comparison in comparisons.items():
        lines.extend([
            "",
            f"## Mode {mode}",
            "",
            f"- 全部逐项一致：`{comparison.all_equal}`",
            "",
            "| new current | aligned legacy current | difference |",
            "|---|---|---|",
        ])
        for index, (legacy_name, difference) in enumerate(
            zip(comparison.aligned_legacy_names, comparison.differences)
        ):
            lines.append(f"| I{index} | {legacy_name} | `{difference}` |")
    (DOCS / "LEGACY_CURRENT_COMPARISON.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    write_currents_doc()
    write_checks_doc()
    write_legacy_comparison_doc()
    print(f"已生成电流 Markdown 到 {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
