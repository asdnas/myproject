# A-H 八模态归一化分段电流

## 归一化定义

- 本文使用 `K = n*V2/V1` 表示电压变比；不在新模块中使用参考文献常见的 `M`，以避免与本文符号体系混淆。
- `Ts = 1/fs`，`Ths = Ts/2`。
- `Ib = V1/(4*fs*L) = V1*Ts/(4*L)`。
- `Pb = n*V1*V2/(8*fs*L)`；`p_star` 已在 `normalized_metrics.py` 中实现并与表 A1 对照。
- `tau_k = duration_k/Ths`，完整周期满足 `sum(tau_k)=2`。
- `vL_star_k = v1_state_k - K*v2_state_k`。
- `delta_I_star_k = 2*vL_star_k*tau_k`。
- `I_(k+1)_star = I_k_star + delta_I_star_k`。
- 零平均电流约束：`sum((I_k_star + I_(k+1)_star)*tau_k/2)=0`。

## 总体验证

| mode | sum(tau) | sum(tau)-2 | sum(delta I*) | I8*-I0* | normalized area | I/Ib consistency |
|---|---:|---:|---:|---:|---:|---|
| A | `2` | `0` | `0` | `0` | `0` | True |
| B | `2` | `0` | `0` | `0` | `0` | True |
| C | `2` | `0` | `0` | `0` | `0` | True |
| D | `2` | `0` | `0` | `0` | `0` | True |
| E | `2` | `0` | `0` | `0` | `0` | True |
| F | `2` | `0` | `0` | `0` | `0` | True |
| G | `2` | `0` | `0` | `0` | `0` | True |
| H | `2` | `0` | `0` | `0` | `0` | True |

## D/G Legacy 与已有结果

- D 模式已有有量纲结果与 legacy 周期对齐后逐项一致：`True`。
- G 模式已有有量纲结果与 legacy 周期对齐后逐项一致：`True`。
- 本次直接无量纲递推又与已有有量纲结果除以 `Ib` 后逐项一致，因此 D/G 归一化结果间接通过 legacy 回归验证。

## Mode A

- `I0_star = D1 + D2*K`
- LaTeX: `$D_{1} + D_{2} K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `(D1 - D2 + 2*phi - 2)/2` | -1 | 0 | `-1` | `-D1 + D2 - 2*phi + 2` |
| 2 | `D2` | -1 | 1 | `-K - 1` | `-2*D2*(K + 1)` |
| 3 | `(D1 - D2 - 2*phi + 2)/2` | -1 | 0 | `-1` | `-D1 + D2 + 2*phi - 2` |
| 4 | `1 - D1` | 0 | 0 | `0` | `0` |
| 5 | `(D1 - D2 + 2*phi - 2)/2` | 1 | 0 | `1` | `D1 - D2 + 2*phi - 2` |
| 6 | `D2` | 1 | -1 | `K + 1` | `2*D2*(K + 1)` |
| 7 | `(D1 - D2 - 2*phi + 2)/2` | 1 | 0 | `1` | `D1 - D2 - 2*phi + 2` |
| 8 | `1 - D1` | 0 | 0 | `0` | `0` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I1_star | `D2*K + D2 - 2*phi + 2` | `$D_{2} K + D_{2} - 2 \phi + 2$` |
| I2_star | `-D2*K - D2 - 2*phi + 2` | `$- D_{2} K - D_{2} - 2 \phi + 2$` |
| I3_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I4_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I5_star | `-D2*K - D2 + 2*phi - 2` | `$- D_{2} K - D_{2} + 2 \phi - 2$` |
| I6_star | `D2*K + D2 + 2*phi - 2` | `$D_{2} K + D_{2} + 2 \phi - 2$` |
| I7_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I8_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |

## Mode B

- `I0_star = D1*K + D1 + 2*K*phi - 2*K`
- LaTeX: `$D_{1} K + D_{1} + 2 K \phi - 2 K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `(D1 + D2 + 2*phi - 2)/2` | -1 | 1 | `-K - 1` | `-(K + 1)*(D1 + D2 + 2*phi - 2)` |
| 2 | `(D1 - D2 - 2*phi + 2)/2` | -1 | 0 | `-1` | `-D1 + D2 + 2*phi - 2` |
| 3 | `-(D1 + D2 - 2*phi)/2` | 0 | 0 | `0` | `0` |
| 4 | `-(D1 - D2 + 2*phi - 2)/2` | 0 | -1 | `K` | `-K*(D1 - D2 + 2*phi - 2)` |
| 5 | `(D1 + D2 + 2*phi - 2)/2` | 1 | -1 | `K + 1` | `(K + 1)*(D1 + D2 + 2*phi - 2)` |
| 6 | `(D1 - D2 - 2*phi + 2)/2` | 1 | 0 | `1` | `D1 - D2 - 2*phi + 2` |
| 7 | `-(D1 + D2 - 2*phi)/2` | 0 | 0 | `0` | `0` |
| 8 | `-(D1 - D2 + 2*phi - 2)/2` | 0 | 1 | `-K` | `K*(D1 - D2 + 2*phi - 2)` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1*K + D1 + 2*K*phi - 2*K` | `$D_{1} K + D_{1} + 2 K \phi - 2 K$` |
| I1_star | `-D2*K - D2 - 2*phi + 2` | `$- D_{2} K - D_{2} - 2 \phi + 2$` |
| I2_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I3_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I4_star | `-D1*K - D1 - 2*K*phi + 2*K` | `$- D_{1} K - D_{1} - 2 K \phi + 2 K$` |
| I5_star | `D2*K + D2 + 2*phi - 2` | `$D_{2} K + D_{2} + 2 \phi - 2$` |
| I6_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I7_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I8_star | `D1*K + D1 + 2*K*phi - 2*K` | `$D_{1} K + D_{1} + 2 K \phi - 2 K$` |

## Mode C

- `I0_star = D1 - D2*K`
- LaTeX: `$D_{1} - D_{2} K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `D1` | -1 | 0 | `-1` | `-2*D1` |
| 2 | `-(D1 + D2 - 2*phi)/2` | 0 | 0 | `0` | `0` |
| 3 | `D2` | 0 | -1 | `K` | `2*D2*K` |
| 4 | `-(D1 + D2 + 2*phi - 2)/2` | 0 | 0 | `0` | `0` |
| 5 | `D1` | 1 | 0 | `1` | `2*D1` |
| 6 | `-(D1 + D2 - 2*phi)/2` | 0 | 0 | `0` | `0` |
| 7 | `D2` | 0 | 1 | `-K` | `-2*D2*K` |
| 8 | `-(D1 + D2 + 2*phi - 2)/2` | 0 | 0 | `0` | `0` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I1_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I2_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I3_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I4_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I5_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I6_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I7_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I8_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |

## Mode D

- `I0_star = D1*K + D1 + 2*K*phi - 2*K`
- LaTeX: `$D_{1} K + D_{1} + 2 K \phi - 2 K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `(D1 + D2 + 2*phi - 2)/2` | -1 | 1 | `-K - 1` | `-(K + 1)*(D1 + D2 + 2*phi - 2)` |
| 2 | `1 - D2` | -1 | 0 | `-1` | `2*(D2 - 1)` |
| 3 | `(D1 + D2 - 2*phi)/2` | -1 | -1 | `K - 1` | `(K - 1)*(D1 + D2 - 2*phi)` |
| 4 | `1 - D1` | 0 | -1 | `K` | `-2*K*(D1 - 1)` |
| 5 | `(D1 + D2 + 2*phi - 2)/2` | 1 | -1 | `K + 1` | `(K + 1)*(D1 + D2 + 2*phi - 2)` |
| 6 | `1 - D2` | 1 | 0 | `1` | `-2*(D2 - 1)` |
| 7 | `(D1 + D2 - 2*phi)/2` | 1 | 1 | `1 - K` | `-(K - 1)*(D1 + D2 - 2*phi)` |
| 8 | `1 - D1` | 0 | 1 | `-K` | `2*K*(D1 - 1)` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1*K + D1 + 2*K*phi - 2*K` | `$D_{1} K + D_{1} + 2 K \phi - 2 K$` |
| I1_star | `-D2*K - D2 - 2*phi + 2` | `$- D_{2} K - D_{2} - 2 \phi + 2$` |
| I2_star | `-D2*K + D2 - 2*phi` | `$- D_{2} K + D_{2} - 2 \phi$` |
| I3_star | `D1*K - D1 - 2*K*phi` | `$D_{1} K - D_{1} - 2 K \phi$` |
| I4_star | `-D1*K - D1 - 2*K*phi + 2*K` | `$- D_{1} K - D_{1} - 2 K \phi + 2 K$` |
| I5_star | `D2*K + D2 + 2*phi - 2` | `$D_{2} K + D_{2} + 2 \phi - 2$` |
| I6_star | `D2*K - D2 + 2*phi` | `$D_{2} K - D_{2} + 2 \phi$` |
| I7_star | `-D1*K + D1 + 2*K*phi` | `$- D_{1} K + D_{1} + 2 K \phi$` |
| I8_star | `D1*K + D1 + 2*K*phi - 2*K` | `$D_{1} K + D_{1} + 2 K \phi - 2 K$` |

## Mode E

- `I0_star = D1 - D2*K`
- LaTeX: `$D_{1} - D_{2} K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `(D1 - D2 + 2*phi)/2` | -1 | 0 | `-1` | `-D1 + D2 - 2*phi` |
| 2 | `(D1 + D2 - 2*phi)/2` | -1 | -1 | `K - 1` | `(K - 1)*(D1 + D2 - 2*phi)` |
| 3 | `-(D1 - D2 - 2*phi)/2` | 0 | -1 | `K` | `-K*(D1 - D2 - 2*phi)` |
| 4 | `-(D1 + D2 + 2*phi - 2)/2` | 0 | 0 | `0` | `0` |
| 5 | `(D1 - D2 + 2*phi)/2` | 1 | 0 | `1` | `D1 - D2 + 2*phi` |
| 6 | `(D1 + D2 - 2*phi)/2` | 1 | 1 | `1 - K` | `-(K - 1)*(D1 + D2 - 2*phi)` |
| 7 | `-(D1 - D2 - 2*phi)/2` | 0 | 1 | `-K` | `K*(D1 - D2 - 2*phi)` |
| 8 | `-(D1 + D2 + 2*phi - 2)/2` | 0 | 0 | `0` | `0` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I1_star | `-D2*K + D2 - 2*phi` | `$- D_{2} K + D_{2} - 2 \phi$` |
| I2_star | `D1*K - D1 - 2*K*phi` | `$D_{1} K - D_{1} - 2 K \phi$` |
| I3_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I4_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I5_star | `D2*K - D2 + 2*phi` | `$D_{2} K - D_{2} + 2 \phi$` |
| I6_star | `-D1*K + D1 + 2*K*phi` | `$- D_{1} K + D_{1} + 2 K \phi$` |
| I7_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I8_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |

## Mode F

- `I0_star = -D1*K + D1 - 2*K*phi`
- LaTeX: `$- D_{1} K + D_{1} - 2 K \phi$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `D1` | -1 | -1 | `K - 1` | `2*D1*(K - 1)` |
| 2 | `-(D1 - D2 - 2*phi)/2` | 0 | -1 | `K` | `-K*(D1 - D2 - 2*phi)` |
| 3 | `1 - D2` | 0 | 0 | `0` | `0` |
| 4 | `-(D1 - D2 + 2*phi)/2` | 0 | 1 | `-K` | `K*(D1 - D2 + 2*phi)` |
| 5 | `D1` | 1 | 1 | `1 - K` | `-2*D1*(K - 1)` |
| 6 | `-(D1 - D2 - 2*phi)/2` | 0 | 1 | `-K` | `K*(D1 - D2 - 2*phi)` |
| 7 | `1 - D2` | 0 | 0 | `0` | `0` |
| 8 | `-(D1 - D2 + 2*phi)/2` | 0 | -1 | `K` | `-K*(D1 - D2 + 2*phi)` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `-D1*K + D1 - 2*K*phi` | `$- D_{1} K + D_{1} - 2 K \phi$` |
| I1_star | `D1*K - D1 - 2*K*phi` | `$D_{1} K - D_{1} - 2 K \phi$` |
| I2_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I3_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I4_star | `D1*K - D1 + 2*K*phi` | `$D_{1} K - D_{1} + 2 K \phi$` |
| I5_star | `-D1*K + D1 + 2*K*phi` | `$- D_{1} K + D_{1} + 2 K \phi$` |
| I6_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I7_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I8_star | `-D1*K + D1 - 2*K*phi` | `$- D_{1} K + D_{1} - 2 K \phi$` |

## Mode G

- `I0_star = D1 - D2*K`
- LaTeX: `$D_{1} - D_{2} K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `(D1 - D2 + 2*phi)/2` | -1 | 0 | `-1` | `-D1 + D2 - 2*phi` |
| 2 | `D2` | -1 | -1 | `K - 1` | `2*D2*(K - 1)` |
| 3 | `(D1 - D2 - 2*phi)/2` | -1 | 0 | `-1` | `-D1 + D2 + 2*phi` |
| 4 | `1 - D1` | 0 | 0 | `0` | `0` |
| 5 | `(D1 - D2 + 2*phi)/2` | 1 | 0 | `1` | `D1 - D2 + 2*phi` |
| 6 | `D2` | 1 | 1 | `1 - K` | `-2*D2*(K - 1)` |
| 7 | `(D1 - D2 - 2*phi)/2` | 1 | 0 | `1` | `D1 - D2 - 2*phi` |
| 8 | `1 - D1` | 0 | 0 | `0` | `0` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I1_star | `-D2*K + D2 - 2*phi` | `$- D_{2} K + D_{2} - 2 \phi$` |
| I2_star | `D2*K - D2 - 2*phi` | `$D_{2} K - D_{2} - 2 \phi$` |
| I3_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I4_star | `-D1 + D2*K` | `$- D_{1} + D_{2} K$` |
| I5_star | `D2*K - D2 + 2*phi` | `$D_{2} K - D_{2} + 2 \phi$` |
| I6_star | `-D2*K + D2 + 2*phi` | `$- D_{2} K + D_{2} + 2 \phi$` |
| I7_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |
| I8_star | `D1 - D2*K` | `$D_{1} - D_{2} K$` |

## Mode H

- `I0_star = D1*K + D1 + 2*K*phi - 2*K`
- LaTeX: `$D_{1} K + D_{1} + 2 K \phi - 2 K$`

### 归一化分段

| segment | tau | v1 | v2 | vL_star | delta_I_star |
|---:|---|---:|---:|---|---|
| 1 | `D1` | -1 | 1 | `-K - 1` | `-2*D1*(K + 1)` |
| 2 | `-(D1 - D2 - 2*phi + 2)/2` | 0 | 1 | `-K` | `K*(D1 - D2 - 2*phi + 2)` |
| 3 | `1 - D2` | 0 | 0 | `0` | `0` |
| 4 | `-(D1 - D2 + 2*phi - 2)/2` | 0 | -1 | `K` | `-K*(D1 - D2 + 2*phi - 2)` |
| 5 | `D1` | 1 | -1 | `K + 1` | `2*D1*(K + 1)` |
| 6 | `-(D1 - D2 - 2*phi + 2)/2` | 0 | -1 | `K` | `-K*(D1 - D2 - 2*phi + 2)` |
| 7 | `1 - D2` | 0 | 0 | `0` | `0` |
| 8 | `-(D1 - D2 + 2*phi - 2)/2` | 0 | 1 | `-K` | `K*(D1 - D2 + 2*phi - 2)` |

### 归一化边界电流

| edge | plain expression | LaTeX |
|---:|---|---|
| I0_star | `D1*K + D1 + 2*K*phi - 2*K` | `$D_{1} K + D_{1} + 2 K \phi - 2 K$` |
| I1_star | `-D1*K - D1 + 2*K*phi - 2*K` | `$- D_{1} K - D_{1} + 2 K \phi - 2 K$` |
| I2_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I3_star | `-D1 - D2*K` | `$- D_{1} - D_{2} K$` |
| I4_star | `-D1*K - D1 - 2*K*phi + 2*K` | `$- D_{1} K - D_{1} - 2 K \phi + 2 K$` |
| I5_star | `D1*K + D1 - 2*K*phi + 2*K` | `$D_{1} K + D_{1} - 2 K \phi + 2 K$` |
| I6_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I7_star | `D1 + D2*K` | `$D_{1} + D_{2} K$` |
| I8_star | `D1*K + D1 + 2*K*phi - 2*K` | `$D_{1} K + D_{1} + 2 K \phi - 2 K$` |

## 后续归一化指标

- 已定义 `Pb = n*V1*V2/(8*fs*L)`。
- `derive_normalized_power(mode)` 已委托到 `normalized_metrics.py` 的统一实现。
- `p_star`、`Irms_star_sq` 与电流应力的表 A1 对照结果见 `AH_A1_REPRODUCTION_REPORT.md`。
