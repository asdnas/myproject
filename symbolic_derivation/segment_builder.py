"""由事件和状态更新构建符号分段。"""

from dataclasses import dataclass

import sympy as sp

from .events import Event, build_events_duty_equivalent, build_events_traditional_tps
from .symbols import L, V1, V2, n


@dataclass(frozen=True)
class Segment:
    index: int
    start_event: str
    end_event: str
    start_time: sp.Expr
    end_time: sp.Expr
    duration_expr: sp.Expr
    v1_state: int
    v2_state: int
    vL_expr: sp.Expr
    slope_expr: sp.Expr
    zero_duration_possible: bool = False
    note: str = ""


def bridge_states(switch_states: dict[str, int]) -> tuple[int, int]:
    v1 = 1 if switch_states.get("S1") == switch_states.get("S4") == 1 else (
        -1 if switch_states.get("S2") == switch_states.get("S3") == 1 else 0
    )
    v2 = 1 if switch_states.get("Q1") == switch_states.get("Q4") == 1 else (
        -1 if switch_states.get("Q2") == switch_states.get("Q3") == 1 else 0
    )
    return v1, v2


def build_segments(events: list[Event], initial_switch_states: dict[str, int]) -> list[Segment]:
    if len(events) != 9:
        raise NotImplementedError("TODO: 构建 8 段需要含首尾边界的 9 个完整事件。")
    if any(event.time_expr is None for event in events):
        raise NotImplementedError("TODO: 事件绝对时间尚未确认，不能自动生成分段。")

    states = dict(initial_switch_states)
    result = []
    for index, (start, end) in enumerate(zip(events, events[1:]), start=1):
        states.update(start.state_update)
        v1, v2 = bridge_states(states)
        duration = sp.simplify(end.time_expr - start.time_expr)
        # 按本次需求采用 vL = v1*V1 - v2*n*V2；legacy 代码采用加号。
        v_l = sp.simplify(v1 * V1 - v2 * n * V2)
        result.append(
            Segment(index, start.name, end.name, start.time_expr, end.time_expr,
                    duration, v1, v2, v_l, sp.simplify(v_l / L))
        )
    return result


def build_mode_segments(method: str, mode: str) -> list[Segment]:
    builder = {
        "traditional_tps": build_events_traditional_tps,
        "duty_equivalent": build_events_duty_equivalent,
    }.get(method)
    if builder is None:
        raise ValueError(f"未知调制方式: {method}")
    events = builder(mode)
    raise NotImplementedError(
        f"TODO: {method}/{mode} 目前仅有 {len(events)} 个关键事件；"
        "完整事件时间和 initial_switch_states 尚待确认。"
    )
