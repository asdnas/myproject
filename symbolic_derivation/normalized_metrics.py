"""基于归一化 VoltageSegment 电流自动推导功率、RMS 与电流应力候选。"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import csv

import sympy as sp

from .normalized_current import K, derive_normalized_current
from .symbols import D1, D2, phi


ALLOWED_SYMBOLS = {K, D1, D2, phi}


@dataclass(frozen=True)
class NormalizedMetrics:
    mode: str
    p_star_expr: sp.Expr
    irms_star_sq_expr: sp.Expr
    current_stress_candidates_star: tuple[sp.Expr, ...]
    symbols: tuple[str, ...]
    dimensional_symbol_check: bool


def _clean(expr: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.simplify(expr)))


def derive_normalized_power(mode_label: str) -> sp.Expr:
    solution = derive_normalized_current(mode_label)
    weighted_area = sum(
        segment.v1_state
        * (segment.i_start_star + segment.i_end_star)
        * segment.tau_expr
        / 2
        for segment in solution.segments
    )
    return _clean(weighted_area / K)


def derive_normalized_irms_sq(mode_label: str) -> sp.Expr:
    solution = derive_normalized_current(mode_label)
    integrals = []
    for segment in solution.segments:
        tau = segment.tau_expr
        i_start = segment.i_start_star
        m_star = 2 * segment.vL_star_expr
        integrals.append(
            i_start**2 * tau
            + i_start * m_star * tau**2
            + m_star**2 * tau**3 / 3
        )
    return _clean(sum(integrals) / 2)


def get_current_stress_candidates_star(mode_label: str) -> tuple[sp.Expr, ...]:
    return tuple(_clean(value) for value in derive_normalized_current(mode_label).currents_star)


@lru_cache(maxsize=8)
def derive_normalized_metrics(mode_label: str) -> NormalizedMetrics:
    mode = mode_label.upper()
    p_star = derive_normalized_power(mode)
    irms_sq = derive_normalized_irms_sq(mode)
    candidates = get_current_stress_candidates_star(mode)
    symbols = set(p_star.free_symbols) | set(irms_sq.free_symbols)
    for candidate in candidates:
        symbols |= candidate.free_symbols
    return NormalizedMetrics(
        mode=mode,
        p_star_expr=p_star,
        irms_star_sq_expr=irms_sq,
        current_stress_candidates_star=candidates,
        symbols=tuple(sorted(symbol.name for symbol in symbols)),
        dimensional_symbol_check=symbols <= ALLOWED_SYMBOLS,
    )


def derive_all_normalized_metrics() -> dict[str, NormalizedMetrics]:
    return {mode: derive_normalized_metrics(mode) for mode in "ABCDEFGH"}


def lambdify_mode_metrics(mode_label: str) -> dict[str, object]:
    metrics = derive_normalized_metrics(mode_label)
    variables = (D1, D2, phi, K)
    return {
        "p_star": sp.lambdify(variables, metrics.p_star_expr, "math"),
        "irms_star_sq": sp.lambdify(variables, metrics.irms_star_sq_expr, "math"),
        "stress_candidates": tuple(
            sp.lambdify(variables, candidate, "math")
            for candidate in metrics.current_stress_candidates_star
        ),
    }


def export_normalized_metrics(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for mode, metrics in derive_all_normalized_metrics().items():
        rows.append({
            "mode": mode,
            "p_star_expr": str(metrics.p_star_expr),
            "Irms_star_sq_expr": str(metrics.irms_star_sq_expr),
            "I_stress_candidates_star": str(metrics.current_stress_candidates_star),
            "symbols": ",".join(metrics.symbols),
            "dimensional_symbol_check": metrics.dimensional_symbol_check,
        })
    with output_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    output = Path(__file__).resolve().parent / "outputs" / "normalized_metrics_AH.csv"
    export_normalized_metrics(output)
    print(f"已导出 A-H 归一化指标：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
