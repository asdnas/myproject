"""从 DSP 源码生成 duty-equivalent 理想 PWM 边沿和 D/G 电压分段候选。

约定：
- 忽略 dead-band 延时，但保留 POLSEL 决定的 A/B 极性；
- d1=D1、d2=D2、fai=phi；
- case_source_actual: 当前源码，正 phi 时副边滞后 (2phi/3)Th；
- case_corrected_expected: 理论修正，正 phi 时副边滞后 phi*Th。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp

from .mode_constraints import get_mode_constraint
from .order_verifier import _linear_range
from .symbols import D1, D2, L, Th, Ts, V1, V2, n, phi
from .voltage_segments import ModeVoltageSegments, VoltageEdge, VoltageSegment


PHASE_CASES = {
    "case_source_actual": sp.Rational(2, 3) * phi,
    "case_corrected_expected": phi,
}


@dataclass(frozen=True)
class SwitchEdge:
    switch_name: str
    bridge: str
    action: str
    time_expr: sp.Expr
    source_file: str
    source_line_or_note: str
    confidence: str
    note: str = ""


@dataclass(frozen=True)
class SwitchInterval:
    switch_name: str
    on_time_expr: sp.Expr
    off_time_expr: sp.Expr
    source: str
    confidence: str
    note: str = ""


@dataclass(frozen=True)
class DutyEquivalentSegmentResult:
    mode: str
    phase_case: str
    model: ModeVoltageSegments
    fixed_order_under_constraints: bool
    validation_rows: tuple[dict, ...]
    note: str


# POLSEL=2: A=RAW_A, B=!RAW_A；POLSEL=1: A=!RAW_A, B=RAW_A（忽略延时）。
_SWITCH_RAW_RULES = {
    "S1": ("primary", D1 / 2, False, 0, "EPWM1A, POLSEL=2"),
    "S2": ("primary", D1 / 2, True, 0, "EPWM1B, POLSEL=2"),
    "S3": ("primary", 1 - D1 / 2, True, 0, "EPWM2A, POLSEL=1"),
    "S4": ("primary", 1 - D1 / 2, False, 0, "EPWM2B, POLSEL=1"),
    "Q1": ("secondary", D2 / 2, False, None, "EPWM3A, POLSEL=2"),
    "Q2": ("secondary", D2 / 2, True, None, "EPWM3B, POLSEL=2"),
    "Q3": ("secondary", 1 - D2 / 2, True, None, "EPWM4A, POLSEL=1"),
    "Q4": ("secondary", 1 - D2 / 2, False, None, "EPWM4B, POLSEL=1"),
}

_EDGE_TRANSITIONS = {
    "p_neg_on": ("primary", -1),
    "p_neg_off": ("primary", 0),
    "p_pos_on": ("primary", 1),
    "p_pos_off": ("primary", 0),
    "s_neg_on": ("secondary", -1),
    "s_neg_off": ("secondary", 0),
    "s_pos_on": ("secondary", 1),
    "s_pos_off": ("secondary", 0),
}
_EXPECTED_FROM = {
    "p_neg_on": 0, "p_neg_off": -1, "p_pos_on": 0, "p_pos_off": 1,
    "s_neg_on": 0, "s_neg_off": -1, "s_pos_on": 0, "s_pos_off": 1,
}
_MODE_ORDER = {
    "D": ("p_neg_on", "s_pos_off", "s_neg_on", "p_neg_off",
          "p_pos_on", "s_neg_off", "s_pos_on", "p_pos_off"),
    "G": ("p_neg_on", "s_neg_on", "s_neg_off", "p_neg_off",
          "p_pos_on", "s_pos_on", "s_pos_off", "p_pos_off"),
}
_START_BEFORE = {"D": (0, 1), "G": (0, 0)}


def build_duty_equivalent_switch_intervals(
    phase_case: str = "case_source_actual",
) -> tuple[SwitchInterval, ...]:
    """生成 S1...Q4 的理想 RAW 导通区间端点。"""

    phase = _phase_time(phase_case)
    rows = []
    for switch, (bridge, ratio, inverted, offset, source) in _SWITCH_RAW_RULES.items():
        module_phase = phase if offset is None else sp.Integer(offset)
        clear = sp.simplify(module_phase + ratio * Ts / 2)
        set_ = sp.simplify(module_phase + Ts - ratio * Ts / 2)
        on_time, off_time = (clear, set_) if inverted else (set_, clear)
        rows.append(SwitchInterval(
            switch, sp.Mod(on_time, Ts), sp.Mod(off_time, Ts),
            f"用户接线表 + 程序/init.c AQ/DB POLSEL + 程序/llc.cla CMPA/TBPHS；{source}",
            "confirmed" if bridge == "primary" else "inferred",
            "忽略死区；区间可能跨越周期边界。副边 confidence 取决于相移方向候选。",
        ))
    return tuple(rows)


def build_duty_equivalent_pwm_edges(
    phase_case: str = "case_source_actual",
) -> tuple[SwitchEdge, ...]:
    edges = []
    for interval in build_duty_equivalent_switch_intervals(phase_case):
        bridge = "primary" if interval.switch_name.startswith("S") else "secondary"
        edges.extend((
            SwitchEdge(interval.switch_name, bridge, "on", interval.on_time_expr,
                       "程序/init.c + 程序/llc.cla", interval.source,
                       interval.confidence, interval.note),
            SwitchEdge(interval.switch_name, bridge, "off", interval.off_time_expr,
                       "程序/init.c + 程序/llc.cla", interval.source,
                       interval.confidence, interval.note),
        ))
    return tuple(edges)


def build_duty_equivalent_voltage_segments(
    mode_label: str, phase_case: str = "case_source_actual",
) -> DutyEquivalentSegmentResult:
    """按 traditional D/G 边沿身份顺序构造候选，并符号验证该顺序是否成立。"""

    mode = mode_label.upper()
    if mode not in _MODE_ORDER:
        raise NotImplementedError("duty-equivalent 第一阶段仅处理 D/G。")
    q = _phase_in_th(phase_case)
    b = (D1 - D2) / 2 + q
    a = (D1 + D2) / 2 + q
    times = {
        "p_neg_on": sp.Integer(0), "p_neg_off": D1,
        "p_pos_on": sp.Integer(1), "p_pos_off": 1 + D1,
        "s_neg_on": b, "s_neg_off": a, "s_pos_on": b + 1, "s_pos_off": a + 1,
    }
    if mode == "D":
        times["s_pos_off"] -= 2

    order = _MODE_ORDER[mode]
    state = _START_BEFORE[mode]
    states_after, edges = [], []
    for index, edge_type in enumerate(order):
        next_state = _apply_edge(state, edge_type)
        edges.append(VoltageEdge(
            index, f"duty_{phase_case}_{mode}_edge_{index}",
            _EDGE_TRANSITIONS[edge_type][0], state, next_state,
            sp.simplify(times[edge_type] * Th),
            "DSP CMPA/AQ/POLSEL + 用户接线表和变量对应关系",
            f"边沿身份={edge_type}；相移候选={phase_case}。",
        ))
        states_after.append(next_state)
        state = next_state
    if state != _START_BEFORE[mode]:
        raise RuntimeError(f"{mode}/{phase_case} 电压状态未闭合。")

    constraint = get_mode_constraint(mode)
    constraints = constraint.variable_range + constraint.inequalities_sympy
    edge_times = [edge.time_expr for edge in edges] + [Ts]
    segments, validation = [], []
    for index in range(8):
        duration = sp.simplify(edge_times[index + 1] - edge_times[index])
        minimum, maximum = _linear_range(sp.simplify(duration / Th), constraints)
        v1, v2 = states_after[index]
        v_l = sp.simplify(v1 * V1 - v2 * n * V2)
        segments.append(VoltageSegment(
            index + 1, edges[index].name,
            edges[index + 1].name if index < 7 else f"duty_{phase_case}_{mode}_period",
            duration, v1, v2, v_l, sp.simplify(v_l / L),
            abs(minimum) <= 1e-9,
            "DSP CMPA/AQ/POLSEL + 用户补充；按候选顺序构造",
            "若 nonnegative_under_constraints=False，则该模式域内事件顺序不固定。",
        ))
        validation.append({
            "segment_index": index + 1, "duration_expr": duration,
            "minimum_over_Th": minimum, "maximum_over_Th": maximum,
            "nonnegative_under_constraints": minimum >= -1e-9,
        })
    period = VoltageEdge(
        8, f"duty_{phase_case}_{mode}_period", "period_boundary", state,
        states_after[0], Ts, "完整周期闭合",
    )
    fixed = all(row["nonnegative_under_constraints"] for row in validation)
    model = ModeVoltageSegments(
        mode, f"duty-equivalent {phase_case}", states_after[0], tuple(segments),
        tuple(edges), period, constraint.inequalities_raw,
        "忽略死区；d1=D1,d2=D2,fai=phi。"
    )
    return DutyEquivalentSegmentResult(
        mode, phase_case, model, fixed, tuple(validation),
        "固定顺序验证通过。" if fixed else "原表 A1 模式域内存在负持续时间，需重新分区。",
    )


def _phase_in_th(phase_case: str) -> sp.Expr:
    try:
        return PHASE_CASES[phase_case]
    except KeyError as exc:
        raise ValueError(f"未知相移候选: {phase_case}") from exc


def _phase_time(phase_case: str) -> sp.Expr:
    return sp.simplify(_phase_in_th(phase_case) * Th)


def _apply_edge(state: tuple[int, int], edge_type: str) -> tuple[int, int]:
    bridge, target = _EDGE_TRANSITIONS[edge_type]
    position = 0 if bridge == "primary" else 1
    if state[position] != _EXPECTED_FROM[edge_type]:
        raise RuntimeError(f"{edge_type} 起始状态错误: {state}")
    return (target, state[1]) if position == 0 else (state[0], target)


def _print_review() -> None:
    print("CMPA/TBPRD: EPWM1=D1/2, EPWM2=1-D1/2, EPWM3=D2/2, EPWM4=1-D2/2")
    print("case_source_actual: phase_time=phi*Ts/3=(2phi/3)*Th")
    print("case_corrected_expected: phase_time=phi*Ts/2=phi*Th")
    for case in PHASE_CASES:
        print(f"\n{case}:")
        for interval in build_duty_equivalent_switch_intervals(case):
            print(f"  {interval.switch_name}: on={interval.on_time_expr}, off={interval.off_time_expr}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-source", action="store_true")
    parser.add_argument("--mode", choices=("D", "G"))
    parser.add_argument("--phase-case", choices=tuple(PHASE_CASES), default="case_source_actual")
    args = parser.parse_args()
    if args.review_source or not args.mode:
        _print_review()
    if args.mode:
        result = build_duty_equivalent_voltage_segments(args.mode, args.phase_case)
        print(f"{args.mode}/{args.phase_case}: fixed_order={result.fixed_order_under_constraints}")
        for row in result.validation_rows:
            print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
