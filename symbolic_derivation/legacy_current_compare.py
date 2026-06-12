"""D/G 新 VoltageSegment 电流与 legacy engine.py 电流对比。"""

from dataclasses import dataclass

import sympy as sp

from engine import derive_i0

from .current_solver import derive_mode_currents
from .legacy_configs import LEGACY_CONFIGS
from .symbols import D1, D2, L, V1, V2, fs, n, phi


@dataclass(frozen=True)
class LegacyCurrentComparison:
    mode: str
    aligned_legacy_names: tuple[str, ...]
    differences: tuple[sp.Expr, ...]
    all_equal: bool


def compare_legacy_mode_currents(mode_label: str) -> LegacyCurrentComparison:
    mode = mode_label.upper()
    if mode not in LEGACY_CONFIGS:
        raise ValueError("legacy 电流对比仅支持 D/G。")
    _, details = derive_i0(LEGACY_CONFIGS[mode])
    legacy_currents = tuple(_to_new_symbols(value) for value in details["I_list"])
    # 新周期从 legacy boundary 4 开始，按同一物理边界循环对齐。
    aligned_indices = (4, 5, 6, 7, 8, 1, 2, 3, 4)
    aligned = tuple(legacy_currents[index] for index in aligned_indices)
    new = derive_mode_currents(mode).currents
    differences = tuple(sp.simplify(a - b) for a, b in zip(new, aligned))
    return LegacyCurrentComparison(
        mode=mode,
        aligned_legacy_names=tuple(f"legacy_I{index}" for index in aligned_indices),
        differences=differences,
        all_equal=all(value == 0 for value in differences),
    )


def compare_all_legacy_currents() -> dict[str, LegacyCurrentComparison]:
    return {mode: compare_legacy_mode_currents(mode) for mode in ("D", "G")}


def _to_new_symbols(expr: sp.Expr) -> sp.Expr:
    old_symbols = {symbol.name: symbol for symbol in expr.free_symbols}
    replacements = {}
    for symbol in (D1, D2, phi, V1, V2, n, L, fs):
        if symbol.name in old_symbols:
            replacements[old_symbols[symbol.name]] = symbol
    return sp.simplify(expr.subs(replacements))
