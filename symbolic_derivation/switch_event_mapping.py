"""traditional TPS 的 VoltageEdge 到开关事件映射。

图 3 明确标注 S1/S4/Q1/Q4 的开通时刻；互补管开通和所有关断动作由
H 桥互补规则推得，标记为 inferred。
"""

from dataclasses import dataclass

import sympy as sp

from .current_solver import derive_mode_currents
from .events import TRADITIONAL_TPS_KEY_EVENT_ORDER
from .voltage_segments import VoltageEdge, get_mode_voltage_segments
from .symbols import D1, D2, L, V1, V2, fs, n, phi


@dataclass(frozen=True)
class SwitchingEvent:
    mode: str
    edge_index: int
    bridge: str
    voltage_transition: str
    candidate_switch_events: tuple[str, ...]
    confirmed_switch_events: tuple[str, ...]
    current_expr: sp.Expr
    current_latex: str
    confidence: str
    source: str
    note: str = ""


# 每个电压边沿包含一个开通动作和同桥臂互补管的关断动作。
# key_on=True 的开通事件由论文图 3 的 tS1/tS4/tQ1/tQ4 标注确认。
TRANSITION_EVENT_RULES = {
    ("primary", "-1->0"): ("S1", "S2", True),
    ("primary", "0->+1"): ("S4", "S3", True),
    ("primary", "+1->0"): ("S3", "S4", False),
    ("primary", "0->-1"): ("S2", "S1", False),
    ("secondary", "-1->0"): ("Q1", "Q2", True),
    ("secondary", "0->+1"): ("Q4", "Q3", True),
    ("secondary", "+1->0"): ("Q3", "Q4", False),
    ("secondary", "0->-1"): ("Q2", "Q1", False),
}


def map_mode_switching_events(mode_label: str) -> list[SwitchingEvent]:
    mode = mode_label.upper()
    model = get_mode_voltage_segments(mode)
    solution = derive_mode_currents(mode)
    mappings = []
    for edge in model.edge_sequence:
        transition = voltage_transition(edge)
        on_switch, off_switch, key_on = TRANSITION_EVENT_RULES[(edge.bridge, transition)]
        on_event, off_event = f"t{on_switch}", f"{off_switch}_off"
        mappings.append(
            SwitchingEvent(
                mode=mode,
                edge_index=edge.index,
                bridge=edge.bridge,
                voltage_transition=transition,
                candidate_switch_events=(on_event, off_event),
                confirmed_switch_events=(on_event,) if key_on else (),
                current_expr=solution.currents[edge.index],
                current_latex=sp.latex(solution.currents[edge.index]),
                confidence="confirmed" if key_on else "inferred",
                source="参考论文图3关键开通标注 + H桥互补规则" if key_on else "H桥互补规则",
                note="同一 VoltageEdge 上开通与互补管关断共享同一边界电流。",
            )
        )
    _validate_fig3_key_order(mode, mappings)
    return mappings


def map_all_switching_events() -> dict[str, list[SwitchingEvent]]:
    return {mode: map_mode_switching_events(mode) for mode in "ABCDEFGH"}


def validate_switch_event_mappings() -> list[dict]:
    rows = []
    for mode, mappings in map_all_switching_events().items():
        solution = derive_mode_currents(mode)
        for mapping in mappings:
            rows.append({
                "mode": mode,
                "edge_index": mapping.edge_index,
                "confirmed_events": ";".join(mapping.confirmed_switch_events),
                "edge_exists": 0 <= mapping.edge_index < 8,
                "current_matches_edge": sp.simplify(
                    mapping.current_expr - solution.currents[mapping.edge_index]
                ) == 0,
                "confidence": mapping.confidence,
            })
    return rows


def compare_dg_confirmed_currents_to_paper() -> dict[str, dict[str, sp.Expr]]:
    """与参考论文表 1 的 D/G 开通电流标幺表达式比较。"""
    M = sp.symbols("M", real=True)
    current_base = V1 / (4 * fs * L)
    expected = {
        "D": {
            "tS1": D1 * (M - 1) - 2 * M * phi,
            "tS4": -(D1 * (M + 1) + 2 * M * phi - 2 * M),
            "tQ1": D2 * (M + 1) + 2 * phi - 2,
            "tQ4": D2 * (M - 1) + 2 * phi,
        },
        "G": {
            "tS1": -(D1 - M * D2),
            "tS4": -(D1 - M * D2),
            "tQ1": D2 * (M - 1) - 2 * phi,
            "tQ4": D2 * (M - 1) + 2 * phi,
        },
    }
    results = {}
    for mode in ("D", "G"):
        results[mode] = {}
        for mapping in map_mode_switching_events(mode):
            for event in mapping.confirmed_switch_events:
                normalized = sp.simplify(mapping.current_expr.subs(V2, M * V1 / n) / current_base)
                results[mode][event] = sp.simplify(normalized - expected[mode][event])
    return results


def voltage_transition(edge: VoltageEdge) -> str:
    position = 0 if edge.bridge == "primary" else 1
    return f"{_state_text(edge.from_state[position])}->{_state_text(edge.to_state[position])}"


def _validate_fig3_key_order(mode: str, mappings: list[SwitchingEvent]) -> None:
    confirmed = {
        event: mapping.edge_index
        for mapping in mappings
        for event in mapping.confirmed_switch_events
    }
    expected = tuple(f"t{name.removesuffix('_on')}" for name in TRADITIONAL_TPS_KEY_EVENT_ORDER[mode])
    indices = [confirmed[event] for event in expected]
    # 图 3 顺序为循环顺序；允许跨越本程序 t=0 周期边界。
    rotated = indices[indices.index(min(indices)):] + indices[:indices.index(min(indices))]
    wrapped = [rotated[0]]
    for index in rotated[1:]:
        wrapped.append(index if index > wrapped[-1] else index + 8)
    if wrapped != sorted(wrapped):
        raise RuntimeError(f"模式 {mode} 的 confirmed 开通事件与图3循环顺序不一致: {indices}")


def _state_text(value: int) -> str:
    return f"+{value}" if value > 0 else str(value)
