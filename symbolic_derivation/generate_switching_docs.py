"""生成 traditional TPS 开关事件映射与电流文档。"""

from pathlib import Path

import sympy as sp

from .switch_event_mapping import (
    TRANSITION_EVENT_RULES,
    compare_dg_confirmed_currents_to_paper,
    map_all_switching_events,
    validate_switch_event_mappings,
)
from .switching_current_extractor import build_switching_current_rows


DOCS = Path(__file__).resolve().parent / "docs"


def write_rules() -> None:
    lines = [
        "# Traditional TPS 开关事件映射规则",
        "",
        "VoltageEdge 边界电流只是桥输出电压发生跳变时的电感电流。要得到具体开关管的"
        "开通/关断电流，还需要结合 H 桥导通状态、同桥臂互补关系和论文图 3 标注。",
        "",
        "## 基础映射",
        "",
        "| bridge | voltage transition | on event | paired off event | on confidence |",
        "|---|---|---|---|---|",
    ]
    for (bridge, transition), (on_switch, off_switch, key_on) in TRANSITION_EVENT_RULES.items():
        lines.append(
            f"| {bridge} | `{transition}` | `t{on_switch}` | `{off_switch}_off` | "
            f"{'confirmed by Fig.3' if key_on else 'inferred by H-bridge rule'} |"
        )
    lines.extend([
        "",
        "## 置信度定义",
        "",
        "- `confirmed`：图 3 明确标注的 `tS1/tS4/tQ1/tQ4`，且循环顺序与 VoltageEdge 一致。",
        "- `inferred`：由同桥臂互补和电压状态变化推得，但图 3 未直接标注。",
        "- `todo`：现有材料无法确认。当前主要保留死区期间的电流取值约定与关断边界确认。",
        "",
        "所有关断事件当前均为 `inferred`。关断指标仅使用 `Abs(current_expr)`，未加入器件模型。",
    ])
    (DOCS / "SWITCH_EVENT_MAPPING_RULES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_edge_mapping() -> None:
    lines = [
        "# VoltageEdge 到图 3 关键事件映射",
        "",
        "图 3 只明确标注每个模式的四个关键开通事件。互补管开通和关断动作保留为 inferred。",
        "图 3 的关键事件顺序按周期循环理解；由于本程序固定以 `v1:0->-1` 为 `edge_0`，"
        "部分模式的最后一个图 3 事件会出现在本程序周期起点之前，并在下一周期闭合。",
    ]
    for mode, mappings in map_all_switching_events().items():
        lines.extend([
            "",
            f"## Mode {mode}",
            "",
            "| edge | transition | edge current | candidates | confirmed | confidence |",
            "|---:|---|---|---|---|---|",
        ])
        for mapping in mappings:
            lines.append(
                f"| {mapping.edge_index} | `{mapping.voltage_transition}` | `I{mapping.edge_index}` | "
                f"`{'; '.join(mapping.candidate_switch_events)}` | "
                f"`{'; '.join(mapping.confirmed_switch_events) or 'none'}` | {mapping.confidence} |"
            )
    lines.extend([
        "",
        "## 人工复核",
        "",
        "- 确认图 3 未标注的互补管开通事件命名。",
        "- 确认是否按理想互补将关断动作与 VoltageEdge 视为同一时刻。",
        "- 确认死区存在时，开通/关断电流采用死区前、死区后还是换流过程中的电流。",
    ])
    (DOCS / "VOLTAGE_EDGE_TO_FIG3_EVENT_MAPPING.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_turn_on() -> None:
    on_rows, _, _ = build_switching_current_rows()
    paper = compare_dg_confirmed_currents_to_paper()
    lines = [
        "# Traditional TPS 开通电流符号公式",
        "",
        "每个模式有 4 个图 3 confirmed 关键开通事件，以及 4 个由 H 桥规则 inferred 的互补管开通事件。",
        "",
    ]
    for mode in "ABCDEFGH":
        lines.extend([
            f"## Mode {mode}",
            "",
            "| edge | event | confidence | current expression | LaTeX |",
            "|---:|---|---|---|---|",
        ])
        for row in (value for value in on_rows if value["mode"] == mode):
            lines.append(
                f"| {row['edge_index']} | {row['switch_event']} | {row['mapping_confidence']} | "
                f"`{row['current_expr']}` | `${row['current_latex']}$` |"
            )
        lines.append("")
    lines.extend([
        "## D/G 论文表 1 核对",
        "",
    ])
    for mode, differences in paper.items():
        lines.append(f"- Mode {mode}: " + ", ".join(f"{event} 差值=`{diff}`" for event, diff in differences.items()))
    lines.append("")
    lines.append("图 3 未标注的 inferred 开通项已同时写入 `switch_event_mapping_todo.csv`。")
    (DOCS / "TURN_ON_CURRENTS_SYMBOLIC.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_turn_off() -> None:
    _, off_rows, _ = build_switching_current_rows()
    lines = [
        "# Traditional TPS 候选关断电流符号公式",
        "",
        "图 3 未直接标注关断事件，因此当前全部关断映射均为 `inferred`。",
        "`turn_off_index_expr=Abs(current_expr)` 仅为形式化指标，后续数值代入后可用于比较。",
        "",
    ]
    for mode in "ABCDEFGH":
        lines.extend([
            f"## Mode {mode}",
            "",
            "| edge | candidate off event | current expression | turn-off index | confidence |",
            "|---:|---|---|---|---|",
        ])
        for row in (value for value in off_rows if value["mode"] == mode):
            lines.append(
                f"| {row['edge_index']} | {row['candidate_switch_event']} | "
                f"`{row['current_expr']}` | `{row['turn_off_index_expr']}` | "
                f"{row['mapping_confidence']} |"
            )
        lines.append("")
    (DOCS / "TURN_OFF_CURRENTS_SYMBOLIC.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    checks = validate_switch_event_mappings()
    if not all(row["edge_exists"] and row["current_matches_edge"] for row in checks):
        raise RuntimeError("开关事件映射校验失败。")
    write_rules()
    write_edge_mapping()
    write_turn_on()
    write_turn_off()
    print(f"已生成 traditional TPS 开关映射文档到 {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
