"""比较 legacy 人工分段与新自动分段。"""

import sympy as sp


def compare_segments(legacy_segments, generated_segments) -> list[str]:
    if generated_segments is None:
        return ["TODO: 自动事件分段尚不可生成，无法与 legacy DnG 人工参数比较。"]
    differences = []
    for old, new in zip(legacy_segments, generated_segments):
        for field in ("duration_expr", "v1_state", "v2_state", "slope_expr"):
            old_value, new_value = getattr(old, field), getattr(new, field)
            if sp.simplify(old_value - new_value) != 0:
                differences.append(f"segment {old.index} {field}: {old_value} != {new_value}")
    return differences
