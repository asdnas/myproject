"""
DAB 电流计算 — 输出 I0~I8 标幺化代数表达式
IN = V1 / (4*fs*L),  M = n*V2/V1
运行方式: python run_example.py
"""
import sympy as sp
from engine import derive_i0
from config import MODE_CONFIG

if __name__ == '__main__':
    # 符号推导
    I0_expr, details = derive_i0(MODE_CONFIG)

    # 标幺化变量
    V1, V2, n_sym, L, fs = sp.symbols('V1 V2 n L fs', positive=True, real=True)
    M_sym = sp.symbols('M')
    IN = V1 / (4 * fs * L)

    # 替换：V2 = M * V1 / n
    subs_v2 = {V2: M_sym * V1 / n_sym}

    print(f"Mode: {MODE_CONFIG['name']}")
    print(f"IN = V1 / (4*fs*L),  M = n*V2/V1\n")
    print("=" * 60)

    for i, I_expr in enumerate(details['I_list']):
        I_pu = sp.simplify(I_expr.subs(subs_v2) / IN)
        print(f"\nI{i}/IN =")
        sp.pprint(I_pu)
