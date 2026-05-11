"""
DAB 电流计算 — 可视化模块
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def plot_waveform(result, save_path=None, show=True):
    """绘制电感电流波形

    参数
    ----
    result : dict
        evaluate() 返回的结果字典
    save_path : str, optional
        保存图片的路径
    show : bool
        是否显示图片
    """
    t_data = result['t_waveform']
    i_data = result['i_waveform']
    I_vals = result['I_values']
    t_vals = result['t_values']

    fig, ax = plt.subplots(figsize=(12, 5))

    # 电流波形
    ax.plot(t_data * 1e6, i_data, 'b-', linewidth=2, label='$i_L$ (A)')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)

    # 标注拐点
    cum_t = 0.0
    colors = plt.cm.tab10(np.linspace(0, 1, 9))
    for i in range(9):
        ax.plot(cum_t * 1e6, I_vals[i], 'o', color=colors[i], markersize=8, zorder=5)
        offset = 14 if i % 2 == 0 else -18
        ax.annotate(
            f'$I_{i}$={I_vals[i]:.2f}A',
            (cum_t * 1e6, I_vals[i]),
            textcoords="offset points",
            xytext=(0, offset),
            fontsize=9,
            ha='center',
            color=colors[i],
            fontweight='bold',
        )
        if i < 8:
            cum_t += t_vals[i]

    # 段边界竖线
    cum_t = 0.0
    for i in range(9):
        ax.axvline(x=cum_t * 1e6, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
        if i < 8:
            cum_t += t_vals[i]

    ax.set_xlabel('时间 (μs)', fontsize=12)
    ax.set_ylabel('电感电流 (A)', fontsize=12)
    ax.set_title('电感电流波形（半周期）', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig
