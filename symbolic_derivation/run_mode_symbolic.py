"""符号推导命令行入口。"""

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from symbolic_derivation.current_solver import (
    derive_mode_currents,
    export_mode_current_csvs,
    segments_from_legacy_config,
    solve_currents,
)
from symbolic_derivation.events import build_events_duty_equivalent
from symbolic_derivation.legacy_configs import LEGACY_CONFIGS
from symbolic_derivation.mode_constraints import get_mode_constraint
from symbolic_derivation.voltage_segments import get_mode_voltage_segments


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=("traditional_tps", "duty_equivalent"), required=True)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--mode", choices=tuple("ABCDEFGH"))
    modes.add_argument("--all-modes", action="store_true")
    parser.add_argument("--derive-current", action="store_true")
    parser.add_argument("--map-switch-events", action="store_true")
    parser.add_argument("--legacy-dng", action="store_true",
                        help="使用当前 config.py 人工 DnG 参数复算电流。")
    args = parser.parse_args()

    selected_modes = tuple("ABCDEFGH") if args.all_modes else (args.mode,)
    if args.method == "duty_equivalent":
        try:
            build_events_duty_equivalent(selected_modes[0])
        except NotImplementedError as exc:
            print(exc)
        return 0

    for mode in selected_modes:
        constraint = get_mode_constraint(mode)
        print(f"Mode {mode} constraint: {constraint.inequalities_raw}")
        model = get_mode_voltage_segments(mode)
        print("Physical voltage edges:")
        for edge in (*model.edge_sequence, model.period_boundary):
            print(f"  {edge.name}: t={edge.time_expr}, {edge.bridge}, "
                  f"{edge.from_state}->{edge.to_state}")
        print(f"Generated {len(model.segments)} physical VoltageSegments.")
        if args.derive_current:
            try:
                solution = derive_mode_currents(mode)
            except Exception as exc:
                print(f"ERROR: 模式 {mode} 电流符号推导失败: {exc}")
                return 1
            print(f"Mode {mode} I0 = {solution.i0_expr}")
            for index, current in enumerate(solution.currents):
                print(f"edge_{index}_current / I{index} = {current}")
            print(f"Checks: total_time-Ts={solution.total_time_minus_ts}, "
                  f"sum(k*dt)={solution.sum_delta_i_expr}, I8-I0={solution.i8_minus_i0}")

    if args.derive_current:
        output_dir = Path(__file__).resolve().parent / "outputs"
        try:
            export_mode_current_csvs(output_dir)
            from symbolic_derivation.generate_current_docs import main as generate_current_docs
            generate_current_docs()
        except Exception as exc:
            print(f"ERROR: 批量电流结果导出失败: {exc}")
            return 1
        print(f"已导出批量电流 CSV 到 {output_dir}")

    if args.map_switch_events:
        from symbolic_derivation.generate_switching_docs import main as generate_switching_docs
        from symbolic_derivation.switching_current_extractor import export_switching_current_csvs
        try:
            export_switching_current_csvs()
            generate_switching_docs()
        except Exception as exc:
            print(f"ERROR: traditional TPS 开关事件映射导出失败: {exc}")
            return 1
        print("已导出 traditional TPS 开关事件映射。")

    if args.legacy_dng:
        if len(selected_modes) != 1 or selected_modes[0] not in LEGACY_CONFIGS:
            print("TODO: --legacy-dng 仅支持单独选择 D 或 G。")
            return 0
        mode = selected_modes[0]
        solution = solve_currents(segments_from_legacy_config(LEGACY_CONFIGS[mode]))
        print(f"Legacy {mode} I0 =", solution.i0_expr)
        for index, current in enumerate(solution.currents):
            print(f"I{index} = {current}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
