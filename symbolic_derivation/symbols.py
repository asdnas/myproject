"""项目统一使用的 SymPy 符号和时间基准。"""

import sympy as sp

D1, D2, phi = sp.symbols("D1 D2 phi", real=True)
V1, V2, n, L, fs = sp.symbols("V1 V2 n L fs", positive=True, real=True)
Ts = 1 / fs
Th = Ts / 2
I0 = sp.symbols("I0", real=True)

VARIABLE_RANGE = (
    sp.Ge(D1, 0),
    sp.Le(D1, 1),
    sp.Ge(D2, 0),
    sp.Le(D2, 1),
    sp.Ge(phi, 0),
    sp.Le(phi, 1),
)
