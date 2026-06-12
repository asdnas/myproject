"""导出 traditional TPS 开通、关断与待确认映射。"""

import csv
from pathlib import Path

import sympy as sp

from .switch_event_mapping import (
    TRANSITION_EVENT_RULES,
    map_all_switching_events,
    validate_switch_event_mappings,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def build_switching_current_rows() -> tuple[list[dict], list[dict], list[dict]]:
    turn_on, turn_off, todo = [], [], []
    for mode, mappings in map_all_switching_events().items():
        for mapping in mappings:
            on_switch, off_switch, key_on = TRANSITION_EVENT_RULES[
                (mapping.bridge, mapping.voltage_transition)
            ]
            on_confidence = "confirmed" if key_on else "inferred"
            turn_on.append({
                "mode": mode,
                "edge_index": mapping.edge_index,
                "edge_current_name": f"I{mapping.edge_index}",
                "switch_event": f"t{on_switch}",
                "switch_name": on_switch,
                "action": "on",
                "bridge": mapping.bridge,
                "voltage_transition": mapping.voltage_transition,
                "current_expr": str(mapping.current_expr),
                "current_latex": mapping.current_latex,
                "mapping_confidence": on_confidence,
                "source": mapping.source if key_on else "H桥互补规则",
                "note": "图3关键开通标注确认。" if key_on else "图3未标注该互补管开通；由H桥规则推得。",
            })
            turn_off.append({
                "mode": mode,
                "edge_index": mapping.edge_index,
                "edge_current_name": f"I{mapping.edge_index}",
                "candidate_switch_event": f"{off_switch}_off",
                "switch_name": off_switch,
                "action": "off",
                "bridge": mapping.bridge,
                "voltage_transition": mapping.voltage_transition,
                "current_expr": str(mapping.current_expr),
                "current_latex": mapping.current_latex,
                "mapping_confidence": "inferred",
                "turn_off_index_expr": str(sp.Abs(mapping.current_expr)),
                "note": "由同桥臂互补规则推得；图3未直接标注关断事件。",
            })
            if not key_on:
                todo.append({
                    "mode": mode,
                    "edge_index": mapping.edge_index,
                    "bridge": mapping.bridge,
                    "voltage_transition": mapping.voltage_transition,
                    "edge_current_name": f"I{mapping.edge_index}",
                    "possible_events": f"t{on_switch}; {off_switch}_off",
                    "why_uncertain": "图3未直接标注该互补管开通和对应关断。",
                    "need_user_confirm": "确认互补管事件命名及死区期间电流取值约定。",
                })
            todo.append({
                "mode": mode,
                "edge_index": mapping.edge_index,
                "bridge": mapping.bridge,
                "voltage_transition": mapping.voltage_transition,
                "edge_current_name": f"I{mapping.edge_index}",
                "possible_events": f"{off_switch}_off",
                "why_uncertain": "图3主要标注开通点，未直接标注关断动作。",
                "need_user_confirm": "确认关断事件与电压跳变边界是否按理想互补、忽略死区处理。",
            })
    return turn_on, turn_off, todo


def export_switching_current_csvs(output_dir: Path = OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    on_rows, off_rows, todo_rows = build_switching_current_rows()
    _write_csv(output_dir / "turn_on_currents_symbolic.csv", on_rows)
    _write_csv(output_dir / "turn_off_currents_symbolic.csv", off_rows)
    _write_csv(output_dir / "switch_event_mapping_todo.csv", todo_rows)
    _write_csv(output_dir / "switch_event_mapping_validation.csv", validate_switch_event_mappings())


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    export_switching_current_csvs()
    print(f"已导出 traditional TPS 开关事件映射到 {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
