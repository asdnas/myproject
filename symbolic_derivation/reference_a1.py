"""参考论文附表 A1 的工作特性表达式。

原文使用 M=n*V2/V1；本模块对外统一使用 K。公式来自 `参考论文.pdf`
附录 A 表 A1。G 模式 RMS 的 PDF 文本层存在排版歧义，当前按三次多项式
结构录入候选，并保留人工复核说明。
"""

from dataclasses import dataclass

import sympy as sp

from .mode_constraints import get_mode_constraint
from .normalized_current import K
from .symbols import D1, D2, phi


@dataclass(frozen=True)
class ReferenceA1:
    mode: str
    constraints_raw: str
    p_star_reference: sp.Expr
    current_stress_reference_lt1: sp.Expr
    current_stress_reference_ge1: sp.Expr
    irms_star_sq_reference: sp.Expr
    source: str = "参考论文.pdf 附录 A 表 A1；原文 M 已替换为 K"
    review_status: str = "CONFIRMED_FROM_PDF_TEXT"
    note: str = ""


def _ref(mode, power, stress_lt1, stress_ge1, rms, note="", review_status="CONFIRMED_FROM_PDF_TEXT"):
    return ReferenceA1(
        mode=mode,
        constraints_raw=get_mode_constraint(mode).inequalities_raw,
        p_star_reference=sp.factor(power),
        current_stress_reference_lt1=stress_lt1,
        current_stress_reference_ge1=stress_ge1,
        irms_star_sq_reference=sp.factor(rms),
        review_status=review_status,
        note=note,
    )


REFERENCE_A1 = {
    "A": _ref(
        "A", 4*D2*(1-phi), D1+K*D2, D1+K*D2,
        (-2*D1**3 - 3*D1**2*D2*K + 3*D1**2 + 6*D1*D2*K
         - 2*D2**3*K**2 - D2**3*K + 3*D2**2*K**2
         - 12*D2*K*phi**2 + 24*D2*K*phi - 12*D2*K) / 3,
    ),
    "B": _ref(
        "B", 2*D1*D2 - 2*(phi + (D1+D2)/2 - 1)**2, D1+K*D2, D1+K*D2,
        (-D1**3*K - 4*D1**3 - 3*D1**2*D2*K - 6*D1**2*K*phi
         + 6*D1**2*K + 6*D1**2 - 3*D1*D2**2*K + 12*D1*D2*K*phi
         - 12*D1*K*phi**2 + 24*D1*K*phi - 12*D1*K
         - 4*D2**3*K**2 - D2**3*K + 6*D2**2*K**2
         - 6*D2**2*K*phi + 6*D2**2*K - 12*D2*K*phi**2
         + 24*D2*K*phi - 12*D2*K - 8*K*phi**3
         + 24*K*phi**2 - 24*K*phi + 8*K) / 6,
    ),
    "C": _ref(
        "C", 2*D1*D2, D1+K*D2, D1+K*D2,
        (3*D1**2 - 2*D1**3 + 3*D2**2*K**2 - 2*D2**3*K**2
         - 6*D1*D2*K + 12*D1*D2*K*phi) / 3,
    ),
    "D": _ref(
        "D", 1-(2*phi-1)**2-(D2-1)**2-(D1-1)**2,
        D1-D1*K+2*phi*K, 2*phi-D2+D2*K,
        (-2*D1**3 - 6*D1**2*K*phi + 3*D1**2*K + 3*D1**2
         + 12*D1*K*phi - 6*D1*K - 2*D2**3*K**2 + 3*D2**2*K**2
         - 6*D2**2*K*phi + 3*D2**2*K + 12*D2*K*phi - 6*D2*K
         - 8*K*phi**3 + 12*K*phi**2 - 12*K*phi + 4*K) / 3,
    ),
    "E": _ref(
        "E", -(D1-D2)**2/2 + 2*(D1+D2)*phi - 2*phi**2,
        D1-D1*K+2*phi*K, 2*phi-D2+D2*K,
        (D1**3*K - 4*D1**3 + 3*D1**2*D2*K - 6*D1**2*K*phi
         + 6*D1**2 + 3*D1*D2**2*K + 12*D1*D2*K*phi
         - 12*D1*D2*K + 12*D1*K*phi**2 - 4*D2**3*K**2
         + D2**3*K + 6*D2**2*K**2 - 6*D2**2*K*phi
         + 12*D2*K*phi**2 - 8*K*phi**3) / 6,
    ),
    "F": _ref(
        "F", 4*D1*phi,
        sp.Max(D2*K-D1, D1-D1*K+2*phi*K), D2*K-D1,
        (D1**3*K - 2*D1**3 + 3*D1**2 + 3*D1*D2**2*K
         - 6*D1*D2*K + 12*D1*phi**2*K - 2*D2**3*K**2
         + 3*D2**2*K**2) / 3,
    ),
    "G": _ref(
        "G", 4*D2*phi,
        D1-D2*K, sp.Max(D2*K-D2+2*phi, D1-D2*K),
        (-2*D1**3 + 3*D1**2*D2*K + 3*D1**2 - 6*D1*D2*K
         - 2*D2**3*K**2 + D2**3*K + 3*D2**2*K**2
        + 12*D2*K*phi**2) / 3,
        note="PDF 文本抽取将中间项显示为 `3D1^2D2^2M`；按总次数三次录入为 `3D1^2D2M`，需结合自动对照复核。",
        review_status="NEEDS_MANUAL_REVIEW_PDF_VISUAL",
    ),
    "H": _ref(
        "H", 4*D1*(1-phi), D1+K*D2, D1+K*D2,
        (-D1**3*K - 2*D1**3 + 3*D1**2 - 3*D1*D2**2*K
         + 6*D1*D2*K - 12*D1*K*phi**2 + 24*D1*K*phi
         - 12*D1*K - 2*D2**3*K**2 + 3*D2**2*K**2) / 3,
    ),
}


def get_reference_a1(mode_label: str) -> ReferenceA1:
    return REFERENCE_A1[mode_label.upper()]
