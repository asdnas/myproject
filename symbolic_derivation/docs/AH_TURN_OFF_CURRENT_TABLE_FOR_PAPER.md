# A-H Traditional TPS 关断电流论文总表

全部关断事件映射均为 `inferred`。电流定义为忽略死区的 ideal boundary current；`turn_off_index=Abs(Ioff)`。

## Mode A

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 1 | `I1` | `(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 2 | `I2` | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | $\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 3 | `I3` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 5 | `I5` | `(-D2*V1 - D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{- D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 6 | `I6` | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 7 | `I7` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |

## Mode B

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 1 | `I1` | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | $\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 2 | `I2` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 3 | `I3` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 5 | `I5` | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 6 | `I6` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 7 | `I7` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |

## Mode C

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 1 | `I1` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 2 | `I2` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 5 | `I5` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 6 | `I6` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 7 | `I7` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode D

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 1 | `I1` | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | $\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 2 | `I2` | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | $\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 3 | `I3` | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 5 | `I5` | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 6 | `I6` | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 7 | `I7` | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |

## Mode E

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 1 | `I1` | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | $\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 2 | `I2` | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 5 | `I5` | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 6 | `I6` | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 7 | `I7` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode F

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 - D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | `Abs(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 1 | `I1` | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 2 | `I2` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ | `Abs(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 5 | `I5` | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 6 | `I6` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 7 | `I7` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode G

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 1 | `I1` | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | $\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 2 | `I2` | `(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ | `Abs(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 5 | `I5` | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 6 | `I6` | `(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | `Abs(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 7 | `I7` | `(D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode H

| candidate event | switch | edge | boundary current | plain/simplified expression | LaTeX | turn-off index | confidence |
|---|---|---:|---|---|---|---|---|
| `S1_off` | S1 | 0 | `I0` | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| `S2_off` | S2 | 1 | `I1` | `(-D1*V1 - D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | inferred |
| `Q4_off` | Q4 | 2 | `I2` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q1_off` | Q1 | 3 | `I3` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `S3_off` | S3 | 4 | `I4` | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| `S4_off` | S4 | 5 | `I5` | `(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | inferred |
| `Q2_off` | Q2 | 6 | `I6` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| `Q3_off` | Q3 | 7 | `I7` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |

## LaTeX 表

```latex
\begin{longtable}{ccccc}
Mode & Candidate off event & Edge & Boundary current & Current expression \\
\hline
A & S1_off & 0 & I0 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
A & Q3_off & 1 & I1 & $\frac{D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ \\
A & Q4_off & 2 & I2 & $\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ \\
A & S2_off & 3 & I3 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
A & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
A & Q1_off & 5 & I5 & $\frac{- D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
A & Q2_off & 6 & I6 & $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
A & S4_off & 7 & I7 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
B & S1_off & 0 & I0 & $\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ \\
B & Q4_off & 1 & I1 & $\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ \\
B & S2_off & 2 & I2 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
B & Q1_off & 3 & I3 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
B & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
B & Q2_off & 5 & I5 & $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
B & S4_off & 6 & I6 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
B & Q3_off & 7 & I7 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & S1_off & 0 & I0 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
C & S2_off & 1 & I1 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
C & Q1_off & 2 & I2 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
C & Q2_off & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & S4_off & 5 & I5 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & Q3_off & 6 & I6 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & Q4_off & 7 & I7 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
D & S1_off & 0 & I0 & $\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ \\
D & Q4_off & 1 & I1 & $\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ \\
D & Q1_off & 2 & I2 & $\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ \\
D & S2_off & 3 & I3 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
D & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
D & Q2_off & 5 & I5 & $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
D & Q3_off & 6 & I6 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
D & S4_off & 7 & I7 & $\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ \\
E & S1_off & 0 & I0 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
E & Q1_off & 1 & I1 & $\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ \\
E & S2_off & 2 & I2 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
E & Q2_off & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
E & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
E & Q3_off & 5 & I5 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
E & S4_off & 6 & I6 & $\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ \\
E & Q4_off & 7 & I7 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
F & S1_off & 0 & I0 & $\frac{D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
F & S2_off & 1 & I1 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
F & Q2_off & 2 & I2 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
F & Q3_off & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
F & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ \\
F & S4_off & 5 & I5 & $\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ \\
F & Q4_off & 6 & I6 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
F & Q1_off & 7 & I7 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
G & S1_off & 0 & I0 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
G & Q1_off & 1 & I1 & $\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ \\
G & Q2_off & 2 & I2 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ \\
G & S2_off & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
G & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
G & Q3_off & 5 & I5 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
G & Q4_off & 6 & I6 & $\frac{D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
G & S4_off & 7 & I7 & $\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
H & S1_off & 0 & I0 & $\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ \\
H & S2_off & 1 & I1 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ \\
H & Q4_off & 2 & I2 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
H & Q1_off & 3 & I3 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
H & S3_off & 4 & I4 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
H & S4_off & 5 & I5 & $\frac{D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
H & Q2_off & 6 & I6 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
H & Q3_off & 7 & I7 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
\end{longtable}
```
