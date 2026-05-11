"""
DAB 变换器电流计算引擎
======================
核心算法：8 段梯形面积法推导开关时刻电流 I0 的代数表达式。
"""

import sympy as sp
import numpy as np

# ============================================================
#  符号变量
# ============================================================
V1, V2 = sp.symbols('V1 V2', positive=True, real=True)
n = sp.symbols('n', positive=True, real=True)
L = sp.symbols('L', positive=True, real=True)
fs = sp.symbols('fs', positive=True, real=True)
D1_sym, D2_sym, phi_sym = sp.symbols('D1 D2 phi', real=True)
I0_sym = sp.symbols('I0', real=True)

Th = 1 / (2 * fs)

# lambdify 使用的参数顺序和名称
_SYM_VARS = (V1, V2, n, L, fs, D1_sym, D2_sym, phi_sym)
_SYM_NAMES = ['V1', 'V2', 'n', 'L', 'fs', 'D1', 'D2', 'phi']


def get_slope(a, b):
    """根据电压系数计算斜率表达式

    a, b ∈ {-1, 0, 1}
    斜率 k = (a*V1 + b*n*V2) / L
    """
    return (a * V1 + b * n * V2) / L


def _parse_config(config):
    """解析配置字典，提取斜率和时间系数"""
    segments = config['segments']

    if len(segments) != 8:
        raise ValueError(f"需要恰好 8 段，当前配置有 {len(segments)} 段")

    slope_coeffs = []
    time_coeffs = []

    for i, seg in enumerate(segments):
        a = seg['v1']
        b = seg['v2']
        c = seg['time']

        if a not in (-1, 0, 1) or b not in (-1, 0, 1):
            raise ValueError(
                f"段{i + 1}: v1={a}, v2={b}，电压系数必须是 -1, 0 或 1"
            )
        if len(c) != 4:
            raise ValueError(
                f"段{i + 1}: time 系数必须是 4 个值，当前有 {len(c)} 个"
            )

        slope_coeffs.append((a, b))
        time_coeffs.append(tuple(c))

    return slope_coeffs, time_coeffs


def derive_i0(config):
    """核心算法：推导 I0 的代数表达式

    参数
    ----
    config : dict
        MODE_CONFIG 字典，包含 8 段定义

    返回
    ----
    I0_expr : sympy.Expr
        I0 的代数表达式（已化简）
    details : dict
        包含所有中间计算结果的字典，用于调试和展示
    """
    slope_coeffs, time_coeffs = _parse_config(config)

    # ---- 第 1 步：构建 8 段的斜率 k_i 和时间 t_i ----
    k_list = []
    t_list = []

    for i in range(8):
        a, b = slope_coeffs[i]
        c1, c2, c3, c4 = time_coeffs[i]

        k_i = get_slope(a, b)
        t_i = ((c1 * D1_sym + c2 * D2_sym + c3 * phi_sym + c4) * Th).simplify()

        k_list.append(k_i)
        t_list.append(t_i)

    # ---- 第 2 步：递推构建拐点电流 I0..I8 ----
    I_list = [I0_sym]
    for i in range(8):
        I_next = (I_list[-1] + k_list[i] * t_list[i]).simplify()
        I_list.append(I_next)

    # ---- 第 3 步：计算 8 段梯形面积 ----
    area_list = []
    for i in range(8):
        area_i = ((I_list[i] + I_list[i + 1]) * t_list[i] / 2).simplify()
        area_list.append(area_i)

    # ---- 第 4 步：求和 → 求解 I0 ----
    total_area = sum(area_list)
    total_area_simplified = sp.simplify(total_area)

    solution = sp.solve(total_area_simplified, I0_sym)

    if not solution:
        raise RuntimeError("无法求解 I0，请检查系数配置。可尝试在 config.py 中填入非零系数。")

    I0_expr = solution[0]
    I0_simplified = sp.simplify(I0_expr)

    # 代入 I0 后的 I_list
    I_list_substituted = [expr.subs(I0_sym, I0_simplified).simplify() for expr in I_list]
    I_list_substituted[0] = I0_simplified

    details = {
        't_list': t_list,
        'k_list': k_list,
        'I_list_raw': I_list,
        'I_list': I_list_substituted,
        'area_list': area_list,
        'total_area_raw': total_area_simplified,
    }

    return I0_simplified, details


def evaluate(config, params):
    """代入数值参数，计算所有数值结果

    参数
    ----
    config : dict
        MODE_CONFIG 字典
    params : dict
        数值参数，必须包含: V1, V2, n, L, fs, D1, D2, phi
        例如: {'V1': 240, 'V2': 336, 'n': 1.0, 'L': 8.4e-6,
               'fs': 150e3, 'D1': 0.1, 'D2': 0.05, 'phi': 0.15}

    返回
    ----
    result : dict
        I0: I0 数值
        I_values: [I0, I1, ..., I8] 共 9 个拐点电流
        k_values: [k1, ..., k8] 各段斜率 (A/s)
        t_values: [t1, ..., t8] 各段时长 (s)
        area_values: [area1, ..., area8] 各段梯形面积
        total_area: 总面积（应 ≈ 0，用于验证）
        total_time: 8 段时间之和 (s)
        half_period: 半周期 Th = 1/(2*fs) (s)
        I0_expr: I0 的符号表达式
        t_waveform: 波形时间点数组
        i_waveform: 波形电流点数组
    """
    # 检查参数完整性
    missing = [k for k in _SYM_NAMES if k not in params]
    if missing:
        raise ValueError(f"缺少参数: {missing}")

    # 符号推导
    I0_expr, details = derive_i0(config)

    t_exprs = details['t_list']
    k_exprs = details['k_list']

    # 准备数值
    param_vals = [params[name] for name in _SYM_NAMES]

    # ---- 数值计算 ----
    f_I0 = sp.lambdify(_SYM_VARS, I0_expr, 'numpy')
    I0_val = float(f_I0(*param_vals))

    t_vals = []
    for t_expr in t_exprs:
        f_t = sp.lambdify(_SYM_VARS, t_expr, 'numpy')
        t_vals.append(float(f_t(*param_vals)))

    k_vals = []
    for k_expr in k_exprs:
        f_k = sp.lambdify(_SYM_VARS, k_expr, 'numpy')
        k_vals.append(float(f_k(*param_vals)))

    # 递推拐点电流
    I_vals = [I0_val]
    for i in range(8):
        I_vals.append(I_vals[-1] + k_vals[i] * t_vals[i])

    # 梯形面积
    area_vals = []
    for i in range(8):
        area_vals.append((I_vals[i] + I_vals[i + 1]) * t_vals[i] / 2.0)

    # 生成波形数据
    t_wave, i_wave = _build_waveform(t_vals, I_vals)

    return {
        'I0': I0_val,
        'I_values': I_vals,           # [I0..I8], 共 9 个
        'k_values': k_vals,           # [k1..k8]
        't_values': t_vals,           # [t1..t8]
        'area_values': area_vals,     # [area1..area8]
        'total_area': sum(area_vals),
        'total_time': sum(t_vals),
        'half_period': 1.0 / (2.0 * params['fs']),
        'I0_expr': I0_expr,
        't_waveform': t_wave,
        'i_waveform': i_wave,
    }


def get_waveform(config, params, n_pts_per_seg=20):
    """只获取波形数据（时间数组、电流数组），不打印详细信息"""
    result = evaluate(config, params)
    return result['t_waveform'], result['i_waveform']


def _build_waveform(t_vals, I_vals, n_pts_per_seg=20):
    """根据段时长和拐点电流，生成波形 (时间, 电流) 数据点"""
    t_pts = [0.0]
    i_pts = [I_vals[0]]

    cum_t = 0.0
    for i in range(8):
        t_seg = t_vals[i]
        if t_seg <= 0:
            continue
        for j in range(1, n_pts_per_seg + 1):
            frac = j / n_pts_per_seg
            t_pts.append(cum_t + frac * t_seg)
            i_pts.append(I_vals[i] + frac * (I_vals[i + 1] - I_vals[i]))
        cum_t += t_seg

    return np.array(t_pts), np.array(i_pts)
