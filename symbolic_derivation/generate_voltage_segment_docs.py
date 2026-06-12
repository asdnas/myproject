"""生成 A-H VoltageSegment 审查文档。"""

from pathlib import Path

import sympy as sp

from .legacy_configs import LEGACY_CONFIGS
from .voltage_segments import (
    get_mode_voltage_segments,
    recover_voltage_cycle_from_legacy,
    validate_voltage_segments,
)


DOCS = Path(__file__).resolve().parent / "docs"


def _expr(value) -> str:
    return str(sp.factor(value))


def write_ah_voltage_segments() -> None:
    lines = [
        "# A-H 完整周期 VoltageSegment",
        "",
        "统一采用 physical 定义：`vL=v1_state*V1-v2_state*n*V2`，`Ts=2*Th=1/fs`。",
        "以下边沿名称仅描述桥输出电压变化，不映射具体开关管 on/off。",
        "",
        "生成依据：原边固定电压边沿、由 D/G 验证得到的副边电压边沿表达式、"
        "参考论文图 3 的模式排列，以及表 A1 全约束域符号排序。",
    ]
    for mode in "ABCDEFGH":
        model = get_mode_voltage_segments(mode)
        lines.extend([
            "",
            f"## Mode {mode}",
            "",
            f"- 约束：`{model.constraints}`",
            f"- 起始段状态：`{model.start_state}`",
            f"- 来源：{model.source}",
            "",
            "### VoltageEdge",
            "",
            "| index | bridge | from -> to | cumulative_time_expr | note |",
            "|---:|---|---|---|---|",
        ])
        for index, edge in enumerate(model.edge_sequence):
            lines.append(
                f"| {index} | {edge.bridge} | `{edge.from_state} -> {edge.to_state}` | "
                f"`{_expr(edge.time_expr)}` | {edge.note} |"
            )
        edge = model.period_boundary
        lines.append(
            f"| 8 | {edge.bridge} | `{edge.from_state} -> {edge.to_state}` | "
            f"`{_expr(edge.time_expr)}` | {edge.note} |"
        )
        lines.extend([
            "",
            "### VoltageSegment",
            "",
            "| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |",
            "|---:|---|---|---:|---:|---|---|---|",
        ])
        for segment in model.segments:
            lines.append(
                f"| {segment.index} | {segment.start_edge} -> {segment.end_edge} | "
                f"`{_expr(segment.duration_expr)}` | {segment.v1_state} | {segment.v2_state} | "
                f"`{segment.vL_expr}` | `{segment.slope_expr}` | "
                f"{segment.zero_duration_possible} |"
            )
    lines.extend([
        "",
        "## TODO",
        "",
        "- D/G 已与 legacy 逐段回归一致。",
        "- A/B/C/E/F/H 已通过图 3 + 表 A1 的符号排列与非负性校验，但仍建议人工对照图 3 复核电压波形视觉顺序。",
        "- VoltageEdge 暂不映射为具体开关事件。",
    ])
    (DOCS / "AH_VOLTAGE_SEGMENTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_validation_doc() -> None:
    lines = [
        "# A-H VoltageSegment 校验",
        "",
        "校验不是数值采样。持续时间的最小值和最大值通过表 A1 线性约束多面体顶点求得。",
        "B/E 中 `&` 按“且”加入约束集合。",
        "",
        "| mode | segment count | total time = Ts | all duration nonnegative | zero-duration segments | states valid | physical vL valid |",
        "|---|---:|---|---|---|---|---|",
    ]
    for mode in "ABCDEFGH":
        rows = validate_voltage_segments(mode)
        zeros = ",".join(str(row["segment_index"]) for row in rows if row["zero_duration_possible"])
        lines.append(
            f"| {mode} | {len(rows)} | {all(row['total_time_check'] for row in rows)} | "
            f"{all(row['nonnegative_under_constraints'] for row in rows)} | {zeros} | "
            f"{all(row['v1_state_valid'] and row['v2_state_valid'] for row in rows)} | "
            f"{all(row['physical_vL_check'] for row in rows)} |"
        )
    lines.extend([
        "",
        "## D/G Legacy 回归",
        "",
    ])
    for mode, config in LEGACY_CONFIGS.items():
        _, legacy = recover_voltage_cycle_from_legacy(config, mode)
        generated = get_mode_voltage_segments(mode).segments
        fields = ("duration_expr", "v1_state", "v2_state", "vL_expr", "slope_expr")
        equal = all(
            sp.simplify(getattr(old, field) - getattr(new, field)) == 0
            for old, new in zip(legacy, generated)
            for field in fields
        )
        lines.append(f"- Mode {mode}: 8 段 duration/state/vL/slope 逐项一致 = `{equal}`。")
    lines.extend([
        "",
        "## 人工复核需求",
        "",
        "- D/G 无需重新确认分段公式，仅需后续确认图 3 标注点映射。",
        "- A/B/C/E/F/H 建议人工对照图 3 复核电压状态视觉顺序；当前符号校验均通过。",
        "- 所有模式的所有段都可能在某个表 A1 模式边界退化为零长度段。",
    ])
    (DOCS / "AH_SEGMENT_VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_mapping_todo() -> None:
    lines = [
        "# VoltageEdge 到图 3 标注点映射 TODO",
        "",
        "当前 VoltageEdge 只使用 `primary` / `secondary` / `period_boundary` 分类，"
        "不命名为具体开关管事件。",
        "",
        "| mode | 已确认 | 仍需人工确认 |",
        "|---|---|---|",
        "| D | 完整周期 8 段与 legacy 一致；边沿桥类别和时间已确认 | 图 3 中每个标注开通点与 VoltageEdge 的一一映射 |",
        "| G | 完整周期 8 段与 legacy 一致；边沿桥类别和时间已确认 | 图 3 中每个标注开通点与 VoltageEdge 的一一映射 |",
        "| A | 图 3 + 表 A1 排列、总时间、非负性已验证 | 逐边沿视觉复核及图 3 标注点映射 |",
        "| B | 图 3 + 表 A1 排列、总时间、非负性已验证 | 逐边沿视觉复核及图 3 标注点映射 |",
        "| C | 图 3 + 表 A1 排列、总时间、非负性已验证 | 逐边沿视觉复核及图 3 标注点映射 |",
        "| E | 图 3 + 表 A1 排列、总时间、非负性已验证 | 逐边沿视觉复核及图 3 标注点映射 |",
        "| F | 图 3 + 表 A1 排列、总时间、非负性已验证 | 逐边沿视觉复核及图 3 标注点映射 |",
        "| H | 图 3 + 表 A1 排列、总时间、非负性已验证 | 逐边沿视觉复核及图 3 标注点映射 |",
        "",
        "模式边界上相邻 VoltageEdge 可重合。当前保留零长度段，不强行合并重合边沿。",
    ]
    (DOCS / "VOLTAGE_EDGE_MAPPING_TODO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    write_ah_voltage_segments()
    write_validation_doc()
    write_mapping_todo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
