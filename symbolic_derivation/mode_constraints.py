"""参考论文表 A1 中 A-H 模式的约束条件。"""

from dataclasses import dataclass

import sympy as sp

from .symbols import D1, D2, VARIABLE_RANGE, phi


@dataclass(frozen=True)
class ModeConstraint:
    label: str
    inequalities_raw: str
    inequalities_sympy: tuple[sp.Rel, ...]
    variable_range: tuple[sp.Rel, ...] = VARIABLE_RANGE
    source: str = "参考论文表 A1"
    note: str = ""


MODE_CONSTRAINTS = {
    "A": ModeConstraint(
        "A",
        "1 + (D2 - D1)/2 <= phi <= 1 + (D1 - D2)/2",
        (sp.Ge(phi, 1 + (D2 - D1) / 2), sp.Le(phi, 1 + (D1 - D2) / 2)),
    ),
    "B": ModeConstraint(
        "B",
        "(D1 + D2)/2 <= phi <= 1 + (D2 - D1)/2 & "
        "1 - (D1 + D2)/2 <= phi <= 1 + (D1 - D2)/2",
        (
            sp.Ge(phi, (D1 + D2) / 2),
            sp.Le(phi, 1 + (D2 - D1) / 2),
            sp.Ge(phi, 1 - (D1 + D2) / 2),
            sp.Le(phi, 1 + (D1 - D2) / 2),
        ),
        note="用户已确认：原表 & 表示“且”，两组区间约束必须同时成立。",
    ),
    "C": ModeConstraint(
        "C",
        "(D1 + D2)/2 <= phi <= 1 - (D1 + D2)/2",
        (sp.Ge(phi, (D1 + D2) / 2), sp.Le(phi, 1 - (D1 + D2) / 2)),
    ),
    "D": ModeConstraint(
        "D",
        "1 - (D1 + D2)/2 <= phi <= (D1 + D2)/2",
        (sp.Ge(phi, 1 - (D1 + D2) / 2), sp.Le(phi, (D1 + D2) / 2)),
    ),
    "E": ModeConstraint(
        "E",
        "(D1 - D2)/2 <= phi <= 1 - (D1 + D2)/2 & "
        "(D2 - D1)/2 <= phi <= (D1 + D2)/2",
        (
            sp.Ge(phi, (D1 - D2) / 2),
            sp.Le(phi, 1 - (D1 + D2) / 2),
            sp.Ge(phi, (D2 - D1) / 2),
            sp.Le(phi, (D1 + D2) / 2),
        ),
        note="用户已确认：原表 & 表示“且”，两组区间约束必须同时成立。",
    ),
    "F": ModeConstraint(
        "F",
        "(D1 - D2)/2 <= phi <= (D2 - D1)/2",
        (sp.Ge(phi, (D1 - D2) / 2), sp.Le(phi, (D2 - D1) / 2)),
    ),
    "G": ModeConstraint(
        "G",
        "(D2 - D1)/2 <= phi <= (D1 - D2)/2",
        (sp.Ge(phi, (D2 - D1) / 2), sp.Le(phi, (D1 - D2) / 2)),
    ),
    "H": ModeConstraint(
        "H",
        "1 + (D1 - D2)/2 <= phi <= 1 + (D2 - D1)/2",
        (sp.Ge(phi, 1 + (D1 - D2) / 2), sp.Le(phi, 1 + (D2 - D1) / 2)),
    ),
}


def get_mode_constraint(label: str) -> ModeConstraint:
    return MODE_CONSTRAINTS[label.upper()]
