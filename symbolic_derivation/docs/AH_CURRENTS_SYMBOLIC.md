# A-H VoltageEdge 边界电流符号公式

电流由完整周期 8 段 VoltageSegment 递推，并使用完整周期电流平均值为零的面积约束求 `I0`。
当前 `I0...I8` 仅表示 VoltageEdge 边界电流，尚未映射到具体开关管开通/关断事件。

## Mode A

- `I0 = (D1*V1 + D2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| edge_2_current / I2 | `-(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| edge_3_current / I3 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `-(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| edge_6_current / I6 | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| edge_7_current / I7 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `(D1 - D2 + 2*phi - 2)*(D1*V1 + D2*V1 + 2*D2*V2*n - 2*V1*phi + 2*V1)/(32*L*fs**2)` | `$\frac{\left(2 D_{1} V_{1} + 2 D_{2} V_{2} n - V_{1} \left(D_{1} - D_{2} + 2 \phi - 2\right)\right) \left(D_{1} - D_{2} + 2 \phi - 2\right)}{32 L fs^{2}}$` |
| 2 | `-D2*V1*(phi - 1)/(4*L*fs**2)` | `$\frac{D_{2} V_{1} \left(1 - \phi\right)}{4 L fs^{2}}$` |
| 3 | `-(D1 - D2 - 2*phi + 2)*(D1*V1 + D2*V1 + 2*D2*V2*n + 2*V1*phi - 2*V1)/(32*L*fs**2)` | `$- \frac{\left(2 D_{2} \left(V_{1} + V_{2} n\right) + V_{1} \left(D_{1} - D_{2} + 2 \phi - 2\right)\right) \left(D_{1} - D_{2} - 2 \phi + 2\right)}{32 L fs^{2}}$` |
| 4 | `(D1 - 1)*(D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$\frac{\left(D_{1} - 1\right) \left(D_{1} V_{1} + D_{2} V_{2} n\right)}{8 L fs^{2}}$` |
| 5 | `-(D1 - D2 + 2*phi - 2)*(D1*V1 + D2*V1 + 2*D2*V2*n - 2*V1*phi + 2*V1)/(32*L*fs**2)` | `$- \frac{\left(2 D_{1} V_{1} + 2 D_{2} V_{2} n - V_{1} \left(D_{1} - D_{2} + 2 \phi - 2\right)\right) \left(D_{1} - D_{2} + 2 \phi - 2\right)}{32 L fs^{2}}$` |
| 6 | `D2*V1*(phi - 1)/(4*L*fs**2)` | `$\frac{D_{2} V_{1} \left(\phi - 1\right)}{4 L fs^{2}}$` |
| 7 | `(D1 - D2 - 2*phi + 2)*(D1*V1 + D2*V1 + 2*D2*V2*n + 2*V1*phi - 2*V1)/(32*L*fs**2)` | `$\frac{\left(D_{1} - D_{2} - 2 \phi + 2\right) \left(D_{1} V_{1} + D_{2} V_{1} + 2 D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}\right)}{32 L fs^{2}}$` |
| 8 | `-(D1 - 1)*(D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$- \frac{\left(D_{1} - 1\right) \left(D_{1} V_{1} + D_{2} V_{2} n\right)}{8 L fs^{2}}$` |

## Mode B

- `I0 = (D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `-(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| edge_2_current / I2 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_3_current / I3 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `-(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| edge_6_current / I6 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_7_current / I7 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `(D1 + D2 + 2*phi - 2)*(D1*V1 + D1*V2*n - D2*V1 - D2*V2*n - 2*V1*phi + 2*V1 + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$\frac{\left(D_{1} + D_{2} + 2 \phi - 2\right) \left(2 D_{1} V_{1} + 2 D_{1} V_{2} n + 4 V_{2} n \phi - 4 V_{2} n - \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right)}{32 L fs^{2}}$` |
| 2 | `-(D1 - D2 - 2*phi + 2)*(D1*V1 + D2*V1 + 2*D2*V2*n + 2*V1*phi - 2*V1)/(32*L*fs**2)` | `$\frac{\left(D_{1} - D_{2} - 2 \phi + 2\right) \left(2 D_{1} V_{1} + 2 D_{1} V_{2} n - V_{1} \left(D_{1} - D_{2} - 2 \phi + 2\right) + 4 V_{2} n \phi - 4 V_{2} n - 2 \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right)}{32 L fs^{2}}$` |
| 3 | `(D1*V1 + D2*V2*n)*(D1 + D2 - 2*phi)/(16*L*fs**2)` | `$\frac{D_{1}^{2} V_{1} + D_{1} D_{2} V_{1} + D_{1} D_{2} V_{2} n - 2 D_{1} V_{1} \phi + D_{2}^{2} V_{2} n - 2 D_{2} V_{2} n \phi}{16 L fs^{2}}$` |
| 4 | `(D1 - D2 + 2*phi - 2)*(2*D1*V1 + D1*V2*n + D2*V2*n + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$\frac{\left(V_{1} \left(D_{1} - D_{2} - 2 \phi + 2\right) + \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right) \left(D_{1} - D_{2} + 2 \phi - 2\right)}{32 L fs^{2}}$` |
| 5 | `-(D1 + D2 + 2*phi - 2)*(D1*V1 + D1*V2*n - D2*V1 - D2*V2*n - 2*V1*phi + 2*V1 + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$- \frac{\left(D_{1} + D_{2} + 2 \phi - 2\right) \left(2 D_{1} V_{1} + 2 D_{1} V_{2} n + 4 V_{2} n \phi - 4 V_{2} n - \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right)}{32 L fs^{2}}$` |
| 6 | `(D1 - D2 - 2*phi + 2)*(D1*V1 + D2*V1 + 2*D2*V2*n + 2*V1*phi - 2*V1)/(32*L*fs**2)` | `$\frac{\left(D_{1} - D_{2} - 2 \phi + 2\right) \left(- D_{1} V_{2} n + D_{2} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n + \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right)}{32 L fs^{2}}$` |
| 7 | `-(D1*V1 + D2*V2*n)*(D1 + D2 - 2*phi)/(16*L*fs**2)` | `$- \frac{\left(D_{1} V_{1} + D_{2} V_{2} n\right) \left(D_{1} + D_{2} - 2 \phi\right)}{16 L fs^{2}}$` |
| 8 | `-(D1 - D2 + 2*phi - 2)*(2*D1*V1 + D1*V2*n + D2*V2*n + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} + 2 \phi - 2\right) \left(2 D_{1} V_{1} + D_{1} V_{2} n + D_{2} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n\right)}{32 L fs^{2}}$` |

## Mode C

- `I0 = -(-D1*V1 + D2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_2_current / I2 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_3_current / I3 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_6_current / I6 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_7_current / I7 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `-D1*D2*V2*n/(8*L*fs**2)` | `$- \frac{D_{1} D_{2} V_{2} n}{8 L fs^{2}}$` |
| 2 | `(D1*V1 + D2*V2*n)*(D1 + D2 - 2*phi)/(16*L*fs**2)` | `$\frac{\left(D_{1} V_{1} + D_{2} V_{2} n\right) \left(D_{1} + D_{2} - 2 \phi\right)}{16 L fs^{2}}$` |
| 3 | `-D1*D2*V1/(8*L*fs**2)` | `$- \frac{D_{1} D_{2} V_{1}}{8 L fs^{2}}$` |
| 4 | `-(-D1*V1 + D2*V2*n)*(D1 + D2 + 2*phi - 2)/(16*L*fs**2)` | `$\frac{\left(D_{1} V_{1} - D_{2} V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)}{16 L fs^{2}}$` |
| 5 | `D1*D2*V2*n/(8*L*fs**2)` | `$\frac{D_{1} D_{2} V_{2} n}{8 L fs^{2}}$` |
| 6 | `-(D1*V1 + D2*V2*n)*(D1 + D2 - 2*phi)/(16*L*fs**2)` | `$- \frac{\left(D_{1} V_{1} + D_{2} V_{2} n\right) \left(D_{1} + D_{2} - 2 \phi\right)}{16 L fs^{2}}$` |
| 7 | `D1*D2*V1/(8*L*fs**2)` | `$\frac{D_{1} D_{2} V_{1}}{8 L fs^{2}}$` |
| 8 | `(-D1*V1 + D2*V2*n)*(D1 + D2 + 2*phi - 2)/(16*L*fs**2)` | `$- \frac{\left(D_{1} V_{1} - D_{2} V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)}{16 L fs^{2}}$` |

## Mode D

- `I0 = (D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `-(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| edge_2_current / I2 | `-(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| edge_3_current / I3 | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| edge_4_current / I4 | `-(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| edge_6_current / I6 | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| edge_7_current / I7 | `-(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| edge_8_current / I8 | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `(D1 + D2 + 2*phi - 2)*(D1*V1 + D1*V2*n - D2*V1 - D2*V2*n - 2*V1*phi + 2*V1 + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$\frac{\left(D_{1} + D_{2} + 2 \phi - 2\right) \left(2 D_{1} V_{1} + 2 D_{1} V_{2} n + 4 V_{2} n \phi - 4 V_{2} n - \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right)}{32 L fs^{2}}$` |
| 2 | `(D2 - 1)*(D2*V2*n + 2*V1*phi - V1)/(8*L*fs**2)` | `$\frac{D_{2}^{2} V_{2} n + 2 D_{2} V_{1} \phi - D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + V_{1}}{8 L fs^{2}}$` |
| 3 | `(D1 + D2 - 2*phi)*(-D1*V1 + D1*V2*n + D2*V1 - D2*V2*n - 2*V1*phi - 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(D_{1} + D_{2} - 2 \phi\right) \left(2 D_{1} V_{2} n + 2 V_{1} \left(D_{2} - 1\right) - 2 V_{2} n - \left(V_{1} + V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)\right)}{32 L fs^{2}}$` |
| 4 | `(D1 - 1)*(D1*V1 + 2*V2*n*phi - V2*n)/(8*L*fs**2)` | `$\frac{\left(D_{1} - 1\right) \left(D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi + V_{2} n \left(D_{1} - 1\right)\right)}{8 L fs^{2}}$` |
| 5 | `-(D1 + D2 + 2*phi - 2)*(D1*V1 + D1*V2*n - D2*V1 - D2*V2*n - 2*V1*phi + 2*V1 + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$- \frac{\left(D_{1} + D_{2} + 2 \phi - 2\right) \left(D_{1} V_{1} - D_{1} V_{2} n - D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1} + 2 V_{2} n \phi + 2 V_{2} n \left(D_{1} - 1\right)\right)}{32 L fs^{2}}$` |
| 6 | `-(D2 - 1)*(D2*V2*n + 2*V1*phi - V1)/(8*L*fs**2)` | `$- \frac{\left(D_{2} - 1\right) \left(D_{2} V_{2} n + 2 V_{1} \phi - V_{1}\right)}{8 L fs^{2}}$` |
| 7 | `-(D1 + D2 - 2*phi)*(-D1*V1 + D1*V2*n + D2*V1 - D2*V2*n - 2*V1*phi - 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(D_{1} + D_{2} - 2 \phi\right) \left(D_{1} V_{1} - D_{1} V_{2} n - D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi + 2 V_{2} n \phi\right)}{32 L fs^{2}}$` |
| 8 | `-(D1 - 1)*(D1*V1 + 2*V2*n*phi - V2*n)/(8*L*fs**2)` | `$- \frac{\left(D_{1} - 1\right) \left(D_{1} V_{1} + 2 V_{2} n \phi - V_{2} n\right)}{8 L fs^{2}}$` |

## Mode E

- `I0 = -(-D1*V1 + D2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `-(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| edge_2_current / I2 | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| edge_3_current / I3 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| edge_6_current / I6 | `-(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| edge_7_current / I7 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `-(D1 - D2 + 2*phi)*(-D1*V1 - D2*V1 + 2*D2*V2*n + 2*V1*phi)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} + 2 \phi\right) \left(- 2 D_{1} V_{1} + 2 D_{2} V_{2} n + V_{1} \left(D_{1} - D_{2} + 2 \phi\right)\right)}{32 L fs^{2}}$` |
| 2 | `(D1 + D2 - 2*phi)*(-D1*V1 + D1*V2*n + D2*V1 - D2*V2*n - 2*V1*phi - 2*V2*n*phi)/(32*L*fs**2)` | `$- \frac{\left(D_{1} + D_{2} - 2 \phi\right) \left(- 2 D_{1} V_{1} + 2 D_{2} V_{2} n + 2 V_{1} \left(D_{1} - D_{2} + 2 \phi\right) + \left(V_{1} - V_{2} n\right) \left(D_{1} + D_{2} - 2 \phi\right)\right)}{32 L fs^{2}}$` |
| 3 | `-(D1 - D2 - 2*phi)*(-2*D1*V1 + D1*V2*n + D2*V2*n - 2*V2*n*phi)/(32*L*fs**2)` | `$- \frac{\left(V_{1} \left(D_{1} - D_{2} + 2 \phi\right) + \left(V_{1} - V_{2} n\right) \left(D_{1} + D_{2} - 2 \phi\right)\right) \left(- D_{1} + D_{2} + 2 \phi\right)}{32 L fs^{2}}$` |
| 4 | `-(-D1*V1 + D2*V2*n)*(D1 + D2 + 2*phi - 2)/(16*L*fs**2)` | `$\frac{\left(D_{1} V_{1} - D_{2} V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)}{16 L fs^{2}}$` |
| 5 | `(D1 - D2 + 2*phi)*(-D1*V1 - D2*V1 + 2*D2*V2*n + 2*V1*phi)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} + 2 \phi\right) \left(D_{1} V_{1} + D_{2} V_{1} - 2 D_{2} V_{2} n - 2 V_{1} \phi\right)}{32 L fs^{2}}$` |
| 6 | `-(D1 + D2 - 2*phi)*(-D1*V1 + D1*V2*n + D2*V1 - D2*V2*n - 2*V1*phi - 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(D_{1} + D_{2} - 2 \phi\right) \left(D_{1} V_{1} - D_{1} V_{2} n - D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi + 2 V_{2} n \phi\right)}{32 L fs^{2}}$` |
| 7 | `(D1 - D2 - 2*phi)*(-2*D1*V1 + D1*V2*n + D2*V2*n - 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(- D_{1} + D_{2} + 2 \phi\right) \left(2 D_{1} V_{1} - D_{1} V_{2} n - D_{2} V_{2} n + 2 V_{2} n \phi\right)}{32 L fs^{2}}$` |
| 8 | `(-D1*V1 + D2*V2*n)*(D1 + D2 + 2*phi - 2)/(16*L*fs**2)` | `$- \frac{\left(D_{1} V_{1} - D_{2} V_{2} n\right) \left(D_{1} + D_{2} + 2 \phi - 2\right)}{16 L fs^{2}}$` |

## Mode F

- `I0 = -(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `-(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| edge_1_current / I1 | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| edge_2_current / I2 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_3_current / I3 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| edge_5_current / I5 | `-(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| edge_6_current / I6 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_7_current / I7 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `-(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `-D1*V2*n*phi/(4*L*fs**2)` | `$- \frac{D_{1} V_{2} n \phi}{4 L fs^{2}}$` |
| 2 | `-(D1 - D2 - 2*phi)*(-2*D1*V1 + D1*V2*n + D2*V2*n - 2*V2*n*phi)/(32*L*fs**2)` | `$- \frac{\left(- D_{1} + D_{2} + 2 \phi\right) \left(- 2 D_{1} V_{1} + 2 D_{1} V_{2} n + 4 D_{1} \left(V_{1} - V_{2} n\right) + 4 V_{2} n \phi - V_{2} n \left(- D_{1} + D_{2} + 2 \phi\right)\right)}{32 L fs^{2}}$` |
| 3 | `-(D2 - 1)*(-D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$\frac{D_{1} D_{2} V_{1} - D_{1} V_{1} - D_{2}^{2} V_{2} n + D_{2} V_{2} n}{8 L fs^{2}}$` |
| 4 | `-(D1 - D2 + 2*phi)*(-2*D1*V1 + D1*V2*n + D2*V2*n + 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(2 D_{1} \left(V_{1} - V_{2} n\right) - V_{2} n \left(- D_{1} + D_{2} + 2 \phi\right)\right) \left(D_{1} - D_{2} + 2 \phi\right)}{32 L fs^{2}}$` |
| 5 | `D1*V2*n*phi/(4*L*fs**2)` | `$\frac{D_{1} V_{2} n \phi}{4 L fs^{2}}$` |
| 6 | `(D1 - D2 - 2*phi)*(-2*D1*V1 + D1*V2*n + D2*V2*n - 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(- D_{1} + D_{2} + 2 \phi\right) \left(2 D_{1} V_{1} - 2 D_{1} V_{2} n + 4 V_{2} n \phi - V_{2} n \left(- D_{1} + D_{2} + 2 \phi\right)\right)}{32 L fs^{2}}$` |
| 7 | `(D2 - 1)*(-D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$\frac{- D_{1} D_{2} V_{1} + D_{1} V_{1} + D_{2}^{2} V_{2} n - D_{2} V_{2} n}{8 L fs^{2}}$` |
| 8 | `(D1 - D2 + 2*phi)*(-2*D1*V1 + D1*V2*n + D2*V2*n + 2*V2*n*phi)/(32*L*fs**2)` | `$\frac{\left(D_{1} - D_{2} + 2 \phi\right) \left(- 2 D_{1} V_{1} + 2 D_{1} V_{2} n + V_{2} n \left(- D_{1} + D_{2} + 2 \phi\right)\right)}{32 L fs^{2}}$` |

## Mode G

- `I0 = -(-D1*V1 + D2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `-(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| edge_2_current / I2 | `(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| edge_3_current / I3 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| edge_6_current / I6 | `-(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| edge_7_current / I7 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `-(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `-(D1 - D2 + 2*phi)*(-D1*V1 - D2*V1 + 2*D2*V2*n + 2*V1*phi)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} + 2 \phi\right) \left(- 2 D_{1} V_{1} + 2 D_{2} V_{2} n + V_{1} \left(D_{1} - D_{2} + 2 \phi\right)\right)}{32 L fs^{2}}$` |
| 2 | `-D2*V1*phi/(4*L*fs**2)` | `$- \frac{D_{2} V_{1} \phi}{4 L fs^{2}}$` |
| 3 | `(D1 - D2 - 2*phi)*(-D1*V1 - D2*V1 + 2*D2*V2*n - 2*V1*phi)/(32*L*fs**2)` | `$\frac{\left(2 D_{2} \left(V_{1} - V_{2} n\right) + V_{1} \left(D_{1} - D_{2} + 2 \phi\right)\right) \left(- D_{1} + D_{2} + 2 \phi\right)}{32 L fs^{2}}$` |
| 4 | `-(D1 - 1)*(-D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$\frac{\left(D_{1} - 1\right) \left(D_{1} V_{1} - D_{2} V_{2} n\right)}{8 L fs^{2}}$` |
| 5 | `(D1 - D2 + 2*phi)*(-D1*V1 - D2*V1 + 2*D2*V2*n + 2*V1*phi)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} + 2 \phi\right) \left(D_{1} V_{1} + D_{2} V_{1} - 2 D_{2} V_{2} n - 2 V_{1} \phi\right)}{32 L fs^{2}}$` |
| 6 | `D2*V1*phi/(4*L*fs**2)` | `$\frac{D_{2} V_{1} \phi}{4 L fs^{2}}$` |
| 7 | `-(D1 - D2 - 2*phi)*(-D1*V1 - D2*V1 + 2*D2*V2*n - 2*V1*phi)/(32*L*fs**2)` | `$- \frac{\left(- D_{1} + D_{2} + 2 \phi\right) \left(D_{1} V_{1} + D_{2} V_{1} - 2 D_{2} V_{2} n + 2 V_{1} \phi\right)}{32 L fs^{2}}$` |
| 8 | `(D1 - 1)*(-D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$- \frac{\left(D_{1} - 1\right) \left(D_{1} V_{1} - D_{2} V_{2} n\right)}{8 L fs^{2}}$` |

## Mode H

- `I0 = (D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)`
- LaTeX：`$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$`

### 边界电流

| edge/current | expression | LaTeX |
|---|---|---|
| edge_0_current / I0 | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| edge_1_current / I1 | `-(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| edge_2_current / I2 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_3_current / I3 | `-(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| edge_4_current / I4 | `-(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| edge_5_current / I5 | `(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| edge_6_current / I6 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_7_current / I7 | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| edge_8_current / I8 | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |

### 每段面积

| segment | area expression | LaTeX |
|---:|---|---|
| 1 | `D1*V2*n*(phi - 1)/(4*L*fs**2)` | `$\frac{D_{1} V_{2} n \left(\phi - 1\right)}{4 L fs^{2}}$` |
| 2 | `(D1 - D2 - 2*phi + 2)*(2*D1*V1 + D1*V2*n + D2*V2*n - 2*V2*n*phi + 2*V2*n)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} - 2 \phi + 2\right) \left(2 D_{1} V_{1} + 2 D_{1} V_{2} n - 4 D_{1} \left(V_{1} + V_{2} n\right) + 4 V_{2} n \phi + V_{2} n \left(D_{1} - D_{2} - 2 \phi + 2\right) - 4 V_{2} n\right)}{32 L fs^{2}}$` |
| 3 | `(D2 - 1)*(D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$\frac{D_{1} D_{2} V_{1} - D_{1} V_{1} + D_{2}^{2} V_{2} n - D_{2} V_{2} n}{8 L fs^{2}}$` |
| 4 | `(D1 - D2 + 2*phi - 2)*(2*D1*V1 + D1*V2*n + D2*V2*n + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$\frac{\left(2 D_{1} \left(V_{1} + V_{2} n\right) - V_{2} n \left(D_{1} - D_{2} - 2 \phi + 2\right)\right) \left(D_{1} - D_{2} + 2 \phi - 2\right)}{32 L fs^{2}}$` |
| 5 | `-D1*V2*n*(phi - 1)/(4*L*fs**2)` | `$\frac{D_{1} V_{2} n \left(1 - \phi\right)}{4 L fs^{2}}$` |
| 6 | `-(D1 - D2 - 2*phi + 2)*(2*D1*V1 + D1*V2*n + D2*V2*n - 2*V2*n*phi + 2*V2*n)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} - 2 \phi + 2\right) \left(2 D_{1} V_{1} + D_{1} V_{2} n + D_{2} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n\right)}{32 L fs^{2}}$` |
| 7 | `-(D2 - 1)*(D1*V1 + D2*V2*n)/(8*L*fs**2)` | `$- \frac{\left(D_{2} - 1\right) \left(D_{1} V_{1} + D_{2} V_{2} n\right)}{8 L fs^{2}}$` |
| 8 | `-(D1 - D2 + 2*phi - 2)*(2*D1*V1 + D1*V2*n + D2*V2*n + 2*V2*n*phi - 2*V2*n)/(32*L*fs**2)` | `$- \frac{\left(D_{1} - D_{2} + 2 \phi - 2\right) \left(2 D_{1} V_{1} + D_{1} V_{2} n + D_{2} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n\right)}{32 L fs^{2}}$` |
