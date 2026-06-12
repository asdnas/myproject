"""后续使用的完整开关事件框架。

当前阶段不使用该层生成电压分段；主入口是 voltage_segments.py 中的电压跳变事件。
本文件仅保留论文图 3 已确认的关键开通事件相对顺序，绝对时间继续留空。
"""

from dataclasses import dataclass, field
from typing import Mapping

import sympy as sp


@dataclass(frozen=True)
class Event:
    name: str
    switch: str
    action: str
    bridge: str
    time_expr: sp.Expr | None = None
    state_update: Mapping[str, int] = field(default_factory=dict)
    note: str = ""


TRADITIONAL_TPS_KEY_EVENT_ORDER = {
    "A": ("S1_on", "S4_on", "Q1_on", "Q4_on"),
    "B": ("S1_on", "S4_on", "Q1_on", "Q4_on"),
    "C": ("S1_on", "Q1_on", "S4_on", "Q4_on"),
    "D": ("S1_on", "S4_on", "Q1_on", "Q4_on"),
    "E": ("S1_on", "Q1_on", "S4_on", "Q4_on"),
    "F": ("S1_on", "Q1_on", "Q4_on", "S4_on"),
    "G": ("Q1_on", "S1_on", "S4_on", "Q4_on"),
    "H": ("S1_on", "S4_on", "Q1_on", "Q4_on"),
}


def _key_event(name: str) -> Event:
    switch, action = name.split("_")
    bridge = "primary" if switch.startswith("S") else "secondary"
    return Event(
        name=name,
        switch=switch,
        action=action,
        bridge=bridge,
        note="顺序来源：参考论文图 3；绝对 time_expr 与 state_update 待人工确认。",
    )


def build_events_traditional_tps(mode: str) -> list[Event]:
    """返回图 3 已确认的关键开通事件；完整 8 段事件尚未确认。"""
    label = mode.upper()
    if label not in TRADITIONAL_TPS_KEY_EVENT_ORDER:
        raise ValueError(f"未知模式: {mode}")
    return [_key_event(name) for name in TRADITIONAL_TPS_KEY_EVENT_ORDER[label]]


def build_events_duty_equivalent(mode: str) -> list[Event]:
    raise NotImplementedError(
        "TODO: duty_equivalent 的事件时间、事件顺序和状态更新尚无可确认来源。"
    )
