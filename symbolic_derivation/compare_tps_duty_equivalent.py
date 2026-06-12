"""D/G duty-equivalent 与 traditional TPS 的符号对比。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import sympy as sp

from .current_solver import derive_mode_currents, solve_currents
from .duty_equivalent_edges import PHASE_CASES, build_duty_equivalent_voltage_segments
from .switch_event_mapping import TRANSITION_EVENT_RULES, voltage_transition
from .voltage_segments import get_mode_voltage_segments


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def compare_mode(mode_label: str, phase_case: str) -> dict[str, list[dict]]:
    mode = mode_label.upper()
    duty = build_duty_equivalent_voltage_segments(mode, phase_case)
    tps_model = get_mode_voltage_segments(mode)
    tps_currents = derive_mode_currents(mode)
    duty_currents = solve_currents(list(duty.model.segments))

    segment_rows, current_rows, on_rows, off_rows = [], [], [], []
    for tps, deq in zip(tps_model.segments, duty.model.segments):
        segment_rows.append({
            "mode": mode,
            "phase_case": phase_case,
            "preferred": phase_case == "case_corrected_expected",
            "fixed_order_under_constraints": duty.fixed_order_under_constraints,
            "segment_index": tps.index,
            "duration_tps": str(tps.duration_expr),
            "duration_duty": str(deq.duration_expr),
            "duration_difference": str(sp.simplify(deq.duration_expr - tps.duration_expr)),
            "v1_tps": str(tps.v1_state),
            "v1_duty": str(deq.v1_state),
            "v1_equal": deq.v1_state == tps.v1_state,
            "v2_tps": str(tps.v2_state),
            "v2_duty": str(deq.v2_state),
            "v2_equal": deq.v2_state == tps.v2_state,
            "vL_tps": str(tps.vL_expr),
            "vL_duty": str(deq.vL_expr),
            "vL_difference": str(sp.simplify(deq.vL_expr - tps.vL_expr)),
            "slope_tps": str(tps.slope_expr),
            "slope_duty": str(deq.slope_expr),
            "slope_difference": str(sp.simplify(deq.slope_expr - tps.slope_expr)),
            "note": duty.note,
        })
    for index, (tps_i, duty_i) in enumerate(zip(tps_currents.currents, duty_currents.currents)):
        current_rows.append({
            "mode": mode,
            "phase_case": phase_case,
            "preferred": phase_case == "case_corrected_expected",
            "fixed_order_under_constraints": duty.fixed_order_under_constraints,
            "current_index": index,
            "current_name": f"I{index}",
            "tps_current_expr": str(tps_i),
            "duty_current_expr": str(duty_i),
            "difference_expr": str(sp.simplify(duty_i - tps_i)),
            "equal": sp.simplify(duty_i - tps_i) == 0,
            "note": "D 候选的固定顺序验证失败时，duty 电流仅为形式化候选，不是全 D 域物理解。",
        })

    for tps_edge, duty_edge in zip(tps_model.edge_sequence, duty.model.edge_sequence):
        transition = voltage_transition(tps_edge)
        on_switch, off_switch, key_on = TRANSITION_EVENT_RULES[(tps_edge.bridge, transition)]
        difference = sp.simplify(
            duty_currents.currents[duty_edge.index] - tps_currents.currents[tps_edge.index]
        )
        common = {
            "mode": mode,
            "phase_case": phase_case,
            "preferred": phase_case == "case_corrected_expected",
            "fixed_order_under_constraints": duty.fixed_order_under_constraints,
            "edge_index": tps_edge.index,
            "voltage_transition": transition,
            "tps_current_expr": str(tps_currents.currents[tps_edge.index]),
            "duty_current_expr": str(duty_currents.currents[duty_edge.index]),
            "difference_expr": str(difference),
            "equal": difference == 0,
        }
        if key_on:
            on_rows.append({
                **common,
                "switch_event": f"t{on_switch}",
                "switch_name": on_switch,
                "mapping_confidence": "confirmed",
                "note": "事件身份由 TPS 图3确认；duty 边沿由接线/AQ/POLSEL 推得。",
            })
        off_rows.append({
            **common,
            "candidate_switch_event": f"{off_switch}_off",
            "switch_name": off_switch,
            "mapping_confidence": "inferred",
            "tps_turn_off_index": str(sp.Abs(tps_currents.currents[tps_edge.index])),
            "duty_turn_off_index": str(sp.Abs(duty_currents.currents[duty_edge.index])),
            "note": "忽略死区的理想关断边沿；保持 inferred。",
        })
    return {
        "segments": segment_rows, "currents": current_rows,
        "turn_on": on_rows, "turn_off": off_rows,
    }


def export_comparisons(output_dir: Path = OUTPUT_DIR) -> dict[str, list[dict]]:
    combined = {"segments": [], "currents": [], "turn_on": [], "turn_off": []}
    for mode in ("D", "G"):
        for phase_case in PHASE_CASES:
            result = compare_mode(mode, phase_case)
            for key in combined:
                combined[key].extend(result[key])
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "compare_duty_vs_tps_segments.csv", combined["segments"])
    _write_csv(output_dir / "compare_duty_vs_tps_currents.csv", combined["currents"])
    _write_csv(output_dir / "compare_duty_vs_tps_turn_on.csv", combined["turn_on"])
    _write_csv(output_dir / "compare_duty_vs_tps_turn_off.csv", combined["turn_off"])
    _write_normalized_case_csvs(output_dir, combined)
    return combined


def _write_normalized_case_csvs(output_dir: Path, combined: dict[str, list[dict]]) -> None:
    """按用户指定统一字段导出 source_actual/corrected 对比结果。"""
    specs = {
        "currents": ("current_name", "tps_current_expr", "duty_current_expr", "difference_expr"),
        "turn_on": ("switch_event", "tps_current_expr", "duty_current_expr", "difference_expr"),
        "turn_off": ("candidate_switch_event", "tps_current_expr", "duty_current_expr", "difference_expr"),
    }
    segment_rows = []
    for row in combined["segments"]:
        for item, tps_key, duty_key, diff_key in (
            ("duration", "duration_tps", "duration_duty", "duration_difference"),
            ("v1_state", "v1_tps", "v1_duty", None),
            ("v2_state", "v2_tps", "v2_duty", None),
            ("vL_expr", "vL_tps", "vL_duty", "vL_difference"),
            ("slope_expr", "slope_tps", "slope_duty", "slope_difference"),
        ):
            diff = row[diff_key] if diff_key else (
                "0" if row[tps_key] == row[duty_key] else f"{row[duty_key]} - {row[tps_key]}"
            )
            segment_rows.append({
                "mode": row["mode"],
                "case_name": row["phase_case"],
                "item_name": f"segment_{row['segment_index']}_{item}",
                "tps_expr": row[tps_key],
                "duty_expr": row[duty_key],
                "diff_expr": diff,
                "match_status": str(diff == "0"),
                "note": row["note"],
            })
    _write_csv(output_dir / "compare_source_actual_vs_corrected_segments.csv", segment_rows)
    for kind, (name_key, tps_key, duty_key, diff_key) in specs.items():
        rows = []
        for row in combined[kind]:
            item = row[name_key]
            rows.append({
                "mode": row["mode"],
                "case_name": row["phase_case"],
                "item_name": item,
                "tps_expr": row[tps_key],
                "duty_expr": row[duty_key],
                "diff_expr": row[diff_key],
                "match_status": str(row.get("equal", row[diff_key] == "0")),
                "note": row["note"],
            })
        _write_csv(output_dir / f"compare_source_actual_vs_corrected_{kind}.csv", rows)


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("D", "G"))
    parser.add_argument("--phase-case", choices=tuple(PHASE_CASES), default="case_source_actual")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.all or not args.mode:
        rows = export_comparisons()
        print(f"已导出 D/G 双相移候选对比到 {OUTPUT_DIR}")
        print(f"rows: " + ", ".join(f"{key}={len(value)}" for key, value in rows.items()))
        return 0
    result = compare_mode(args.mode, args.phase_case)
    duty = build_duty_equivalent_voltage_segments(args.mode, args.phase_case)
    print(f"{args.mode}/{args.phase_case}: fixed_order={duty.fixed_order_under_constraints}")
    for row in result["turn_on"]:
        print(f"{row['switch_event']}: difference={row['difference_expr']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
