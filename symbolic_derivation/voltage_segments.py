"""以桥输出电压跳变为核心的符号分段中间层。

新程序统一使用 physical 副边状态：
    vL = v1_state*V1 - v2_state*n*V2

legacy 配置中的副边状态使用相反符号：
    v2_physical = -v2_legacy
"""

from dataclasses import dataclass
from pathlib import Path
import csv

import sympy as sp

from .mode_constraints import get_mode_constraint
from .order_verifier import _linear_range
from .symbols import D1, D2, L, Th, Ts, V1, V2, n, phi


@dataclass(frozen=True)
class VoltageEdge:
    index: int
    name: str
    bridge: str
    from_state: tuple[int, int]
    to_state: tuple[int, int]
    time_expr: sp.Expr
    source: str
    note: str = ""


@dataclass(frozen=True)
class VoltageSegment:
    index: int
    start_edge: str
    end_edge: str
    duration_expr: sp.Expr
    v1_state: int
    v2_state: int
    vL_expr: sp.Expr
    slope_expr: sp.Expr
    zero_duration_possible: bool
    source: str
    note: str = ""


@dataclass(frozen=True)
class ModeVoltageSegments:
    mode_label: str
    source: str
    start_state: tuple[int, int]
    segments: tuple[VoltageSegment, ...]
    edge_sequence: tuple[VoltageEdge, ...]
    period_boundary: VoltageEdge
    constraints: str
    notes: str = ""


# 时间均以 Th 为单位。边沿名称只描述桥输出电压变化，不映射具体开关管。
_P0, _P1, _P2, _P3 = "p_neg_on", "p_neg_off", "p_pos_on", "p_pos_off"
_SN, _SF, _SP, _SPF = "s_neg_on", "s_neg_off", "s_pos_on", "s_pos_off"

MODE_EDGE_ORDER = {
    "A": (_P0, _SP, _SPF, _P1, _P2, _SN, _SF, _P3),
    "B": (_P0, _SPF, _P1, _SN, _P2, _SF, _P3, _SP),
    "C": (_P0, _P1, _SN, _SF, _P2, _P3, _SP, _SPF),
    "D": (_P0, _SPF, _SN, _P1, _P2, _SF, _SP, _P3),
    "E": (_P0, _SN, _P1, _SF, _P2, _SP, _P3, _SPF),
    "F": (_P0, _P1, _SF, _SP, _P2, _P3, _SPF, _SN),
    "G": (_P0, _SN, _SF, _P1, _P2, _SP, _SPF, _P3),
    "H": (_P0, _P1, _SPF, _SN, _P2, _P3, _SF, _SP),
}

MODE_SECONDARY_SHIFTS = {
    "A": {_SN: 0, _SF: 0, _SP: -2, _SPF: -2},
    "B": {_SN: 0, _SF: 0, _SP: 0, _SPF: -2},
    "C": {_SN: 0, _SF: 0, _SP: 0, _SPF: 0},
    "D": {_SN: 0, _SF: 0, _SP: 0, _SPF: -2},
    "E": {_SN: 0, _SF: 0, _SP: 0, _SPF: 0},
    "F": {_SN: 2, _SF: 0, _SP: 0, _SPF: 0},
    "G": {_SN: 0, _SF: 0, _SP: 0, _SPF: 0},
    "H": {_SN: 0, _SF: 0, _SP: 0, _SPF: -2},
}

_EDGE_TRANSITIONS = {
    _P0: ("primary", -1),
    _P1: ("primary", 0),
    _P2: ("primary", 1),
    _P3: ("primary", 0),
    _SN: ("secondary", -1),
    _SF: ("secondary", 0),
    _SP: ("secondary", 1),
    _SPF: ("secondary", 0),
}

_EDGE_EXPECTED_FROM = {
    _P0: 0, _P1: -1, _P2: 0, _P3: 1,
    _SN: 0, _SF: -1, _SP: 0, _SPF: 1,
}

_START_V2 = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0, "F": -1, "G": 0, "H": 1}


def legacy_v2_to_physical(v2_legacy: int) -> int:
    return -v2_legacy


def physical_v2_to_legacy(v2_physical: int) -> int:
    return -v2_physical


def physical_voltage_expressions(v1_state: int, v2_state: int) -> tuple[sp.Expr, sp.Expr]:
    v_l = sp.simplify(v1_state * V1 - v2_state * n * V2)
    return v_l, sp.simplify(v_l / L)


def get_mode_voltage_segments(mode_label: str) -> ModeVoltageSegments:
    """由图 3 的电压边沿排列和表 A1 约束构造完整周期 8 段。"""
    mode = mode_label.upper()
    if mode not in MODE_EDGE_ORDER:
        raise ValueError(f"未知模式: {mode_label}")
    constraint = get_mode_constraint(mode)
    edge_times = _edge_times_in_th(mode)
    order = MODE_EDGE_ORDER[mode]
    states_before = (0, _START_V2[mode])
    states_after = []
    edges = []
    state = states_before
    for index, edge_type in enumerate(order):
        next_state = _apply_edge(state, edge_type)
        edges.append(
            VoltageEdge(
                index=index,
                name=f"{mode}_voltage_edge_{index}",
                bridge=_EDGE_TRANSITIONS[edge_type][0],
                from_state=state,
                to_state=next_state,
                time_expr=sp.simplify(edge_times[edge_type] * Th),
                source="参考论文图3电压波形 + 表A1约束下符号排序",
                note=f"电压边沿类型: {edge_type}；不映射具体开关事件。",
            )
        )
        states_after.append(next_state)
        state = next_state

    if state != states_before:
        raise RuntimeError(f"模式 {mode} 的 8 个电压边沿未闭合: {state} != {states_before}")

    period_boundary = VoltageEdge(
        index=8,
        name=f"{mode}_period_boundary",
        bridge="period_boundary",
        from_state=state,
        to_state=states_after[0],
        time_expr=Ts,
        source="完整周期闭合边界",
        note="与下一周期 t=0 的首个电压边沿相接。",
    )
    times = [edge.time_expr for edge in edges] + [Ts]
    segments = []
    constraints = constraint.variable_range + constraint.inequalities_sympy
    for index in range(8):
        duration = sp.simplify(times[index + 1] - times[index])
        minimum, _ = _linear_range(sp.simplify(duration / Th), constraints)
        v_l, slope = physical_voltage_expressions(*states_after[index])
        segments.append(
            VoltageSegment(
                index=index + 1,
                start_edge=edges[index].name,
                end_edge=edges[index + 1].name if index < 7 else period_boundary.name,
                duration_expr=duration,
                v1_state=states_after[index][0],
                v2_state=states_after[index][1],
                vL_expr=v_l,
                slope_expr=slope,
                zero_duration_possible=abs(minimum) <= 1e-9,
                source="参考论文图3电压波形 + 表A1约束下符号排序",
            )
        )
    return ModeVoltageSegments(
        mode_label=mode,
        source="参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证",
        start_state=states_after[0],
        segments=tuple(segments),
        edge_sequence=tuple(edges),
        period_boundary=period_boundary,
        constraints=constraint.inequalities_raw,
        notes="边沿名称仅描述桥电压变化，不对应具体开关管 on/off。",
    )


def get_voltage_segments(mode_label: str) -> list[VoltageSegment]:
    return list(get_mode_voltage_segments(mode_label).segments)


def get_voltage_edges(mode_label: str, include_period_boundary: bool = True) -> list[VoltageEdge]:
    model = get_mode_voltage_segments(mode_label)
    edges = list(model.edge_sequence)
    if include_period_boundary:
        edges.append(model.period_boundary)
    return edges


def validate_voltage_segments(mode_label: str) -> list[dict]:
    model = get_mode_voltage_segments(mode_label)
    constraint = get_mode_constraint(model.mode_label)
    constraints = constraint.variable_range + constraint.inequalities_sympy
    total_ok = sp.simplify(sum(segment.duration_expr for segment in model.segments) - Ts) == 0
    rows = []
    for segment in model.segments:
        minimum, maximum = _linear_range(sp.simplify(segment.duration_expr / Th), constraints)
        expected_v_l, _ = physical_voltage_expressions(segment.v1_state, segment.v2_state)
        rows.append({
            "mode": model.mode_label,
            "segment_index": segment.index,
            "duration_expr": str(segment.duration_expr),
            "total_time_check": total_ok,
            "nonnegative_under_constraints": minimum >= -1e-9,
            "zero_duration_possible": abs(minimum) <= 1e-9,
            "v1_state_valid": segment.v1_state in (-1, 0, 1),
            "v2_state_valid": segment.v2_state in (-1, 0, 1),
            "physical_vL_check": sp.simplify(segment.vL_expr - expected_v_l) == 0,
            "duration_over_Th_min": minimum,
            "duration_over_Th_max": maximum,
            "notes": segment.note,
        })
    return rows


def export_voltage_segments(mode_label: str, output_path: Path) -> None:
    model = get_mode_voltage_segments(mode_label)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ("mode", "segment_index", "start_edge", "end_edge", "duration_expr",
              "v1_state", "v2_state", "vL_expr", "slope_expr",
              "zero_duration_possible", "source", "note")
    with output_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for segment in model.segments:
            writer.writerow({
                "mode": model.mode_label,
                "segment_index": segment.index,
                "start_edge": segment.start_edge,
                "end_edge": segment.end_edge,
                "duration_expr": segment.duration_expr,
                "v1_state": segment.v1_state,
                "v2_state": segment.v2_state,
                "vL_expr": segment.vL_expr,
                "slope_expr": segment.slope_expr,
                "zero_duration_possible": segment.zero_duration_possible,
                "source": segment.source,
                "note": segment.note,
            })


def recover_voltage_cycle_from_legacy(config: dict, mode: str) -> tuple[list[VoltageEdge], list[VoltageSegment]]:
    """从 legacy D/G 人工分段恢复 physical 电压周期。

    循环旋转后以 legacy 第 5 段为第 1 段。D/G 两组均因此满足：
    t=0 时 v1_state=-1，经过 D1*Th 后原边跳变为 0。
    """
    if mode.upper() not in {"D", "G"}:
        raise ValueError("当前仅确认可从 legacy 恢复 D/G。")
    raw = config["segments"]
    if len(raw) != 8:
        raise ValueError("legacy 配置必须恰好包含 8 段。")
    rotated = raw[4:] + raw[:4]

    durations = [_duration(item["time"]) for item in rotated]
    states = [(item["v1"], legacy_v2_to_physical(item["v2"])) for item in rotated]
    times = [sp.Integer(0)]
    for duration in durations:
        times.append(sp.simplify(times[-1] + duration))
    if sp.simplify(times[-1] - Ts) != 0:
        raise ValueError(f"恢复后的 8 段总时长不是 Ts: {times[-1]}")
    if states[0][0] != -1:
        raise ValueError("恢复起点未满足 v1_state=-1。")

    edges = []
    for index in range(8):
        previous = states[index - 1] if index else states[-1]
        current = states[index]
        edges.append(
            VoltageEdge(
                index=index,
                name=f"{mode.upper()}_voltage_edge_{index}",
                bridge=_changed_bridge(previous, current),
                from_state=previous,
                to_state=current,
                time_expr=times[index],
                source="legacy反推；起点规则来自用户补充，并与参考论文图3核对",
                note="不映射到具体开关管 on/off 事件。",
            )
        )
    edges.append(
        VoltageEdge(
            index=8,
            name=f"{mode.upper()}_period_boundary",
            bridge="period_boundary",
            from_state=states[-1],
            to_state=states[0],
            time_expr=Ts,
            source="完整周期边界",
            note="与 t=0 电压跳变物理等价，用于闭合 8 段。",
        )
    )

    segments = []
    for index, (state, duration) in enumerate(zip(states, durations), start=1):
        v_l, slope = physical_voltage_expressions(*state)
        segments.append(
            VoltageSegment(
                index=index,
                start_edge=edges[index - 1].name,
                end_edge=edges[index].name,
                duration_expr=duration,
                v1_state=state[0],
                v2_state=state[1],
                vL_expr=v_l,
                slope_expr=slope,
                zero_duration_possible=False,
                source="legacy反推并转换为 physical 电压定义",
            )
        )
    return edges, segments


def _duration(coefficients: tuple[float, float, float, float]) -> sp.Expr:
    c1, c2, c3, c0 = (sp.Rational(str(value)) for value in coefficients)
    return sp.simplify((c1 * D1 + c2 * D2 + c3 * phi + c0) * Th)


def _changed_bridge(previous: tuple[int, int], current: tuple[int, int]) -> str:
    primary = previous[0] != current[0]
    secondary = previous[1] != current[1]
    if primary and secondary:
        return "both"
    if primary:
        return "primary"
    if secondary:
        return "secondary"
    return "period_boundary"


def _edge_times_in_th(mode: str) -> dict[str, sp.Expr]:
    b = (D1 - D2) / 2 + phi
    a = (D1 + D2) / 2 + phi
    shifts = MODE_SECONDARY_SHIFTS[mode]
    return {
        _P0: sp.Integer(0),
        _P1: D1,
        _P2: sp.Integer(1),
        _P3: 1 + D1,
        _SN: sp.simplify(b + shifts[_SN]),
        _SF: sp.simplify(a + shifts[_SF]),
        _SP: sp.simplify(b + 1 + shifts[_SP]),
        _SPF: sp.simplify(a + 1 + shifts[_SPF]),
    }


def _apply_edge(state: tuple[int, int], edge_type: str) -> tuple[int, int]:
    bridge, to_value = _EDGE_TRANSITIONS[edge_type]
    position = 0 if bridge == "primary" else 1
    if state[position] != _EDGE_EXPECTED_FROM[edge_type]:
        raise RuntimeError(
            f"电压边沿 {edge_type} 的起始状态不一致: "
            f"{state[position]} != {_EDGE_EXPECTED_FROM[edge_type]}"
        )
    return (to_value, state[1]) if bridge == "primary" else (state[0], to_value)
