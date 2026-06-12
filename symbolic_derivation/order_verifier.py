"""在整个线性模式约束域内验证事件顺序。"""

from dataclasses import dataclass
from itertools import combinations

import sympy as sp

from .events import Event
from .mode_constraints import ModeConstraint
from .symbols import D1, D2, phi


@dataclass(frozen=True)
class OrderResult:
    left: str
    right: str
    status: str
    zero_duration_possible: bool
    note: str = ""


def verify_adjacent_order(events: list[Event], constraint: ModeConstraint) -> list[OrderResult]:
    """验证相邻事件顺序；绝对时间缺失时返回明确 TODO。"""
    results = []
    for left, right in zip(events, events[1:]):
        if left.time_expr is None or right.time_expr is None:
            results.append(OrderResult(left.name, right.name, "TODO", False,
                                       "缺少可确认的绝对事件时间表达式。"))
            continue
        difference = sp.simplify(right.time_expr - left.time_expr)
        minimum, maximum = _linear_range(
            difference, constraint.variable_range + constraint.inequalities_sympy
        )
        tolerance = 1e-9
        if minimum >= -tolerance and maximum <= tolerance:
            status = "always_equal"
        elif minimum >= -tolerance:
            status = "left_before_or_equal"
        elif maximum <= tolerance:
            status = "right_before_or_equal"
        else:
            status = "ambiguous"
        results.append(
            OrderResult(
                left.name,
                right.name,
                status,
                minimum <= tolerance and minimum >= -tolerance,
                f"right-left 范围: [{minimum:.12g}, {maximum:.12g}]",
            )
        )
    return results


def _linear_range(expr: sp.Expr, constraints: tuple[sp.Rel, ...]) -> tuple[float, float]:
    variables = (D1, D2, phi)
    halfspaces = []
    for relation in constraints:
        if isinstance(relation, (sp.GreaterThan, sp.StrictGreaterThan)):
            halfspaces.append(sp.expand(relation.rhs - relation.lhs))
        elif isinstance(relation, (sp.LessThan, sp.StrictLessThan)):
            halfspaces.append(sp.expand(relation.lhs - relation.rhs))
        elif isinstance(relation, sp.Equality):
            raise NotImplementedError("TODO: 当前顺序验证器尚未处理等式约束。")
        else:
            raise TypeError(f"不支持的约束: {relation}")

    vertices = set()
    for active in combinations(halfspaces, len(variables)):
        solutions = sp.linsolve(active, variables)
        for solution in solutions:
            if any(value.free_symbols for value in solution):
                continue
            substitutions = dict(zip(variables, solution))
            if all(float(space.subs(substitutions)) <= 1e-9 for space in halfspaces):
                vertices.add(tuple(sp.simplify(value) for value in solution))
    if not vertices:
        raise RuntimeError("模式约束不可行，或约束域不是可枚举顶点的有界三维多面体。")

    values = [float(expr.subs(dict(zip(variables, vertex)))) for vertex in vertices]
    return min(values), max(values)
