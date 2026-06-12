# A-H Traditional TPS 开通电流论文总表

仅列论文图3映射确认的 `tS1/tS4/tQ1/tQ4`。全部表达式来自已推导的 `I0...I8`。

## Mode A

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tQ4` | Q4 | 1 | `I1` | `(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS1` | S1 | 3 | `I3` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 6 | `I6` | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode B

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tS1` | S1 | 2 | `I2` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 5 | `I5` | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 7 | `I7` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode C

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tS1` | S1 | 1 | `I1` | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 6 | `I6` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode D

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tS1` | S1 | 3 | `I3` | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 5 | `I5` | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 6 | `I6` | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode E

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tS1` | S1 | 2 | `I2` | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 5 | `I5` | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode F

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tS1` | S1 | 1 | `I1` | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 2 | `I2` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode G

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tQ1` | Q1 | 2 | `I2` | `(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS1` | S1 | 3 | `I3` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 5 | `I5` | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ | confirmed_from_fig3_mapping |

## Mode H

| event | switch | edge | boundary current | plain/simplified expression | LaTeX | source |
|---|---|---:|---|---|---|---|
| `tS1` | S1 | 1 | `I1` | `(-D1*V1 - D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tS4` | S4 | 4 | `I4` | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ1` | Q1 | 6 | `I6` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |
| `tQ4` | Q4 | 7 | `I7` | `(D1*V1 + D2*V2*n)/(4*L*fs)` | $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ | confirmed_from_fig3_mapping |

## LaTeX 表

```latex
\begin{longtable}{ccccc}
Mode & Event & Edge & Boundary current & Current expression \\
\hline
A & tQ4 & 1 & I1 & $\frac{D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$ \\
A & tS1 & 3 & I3 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
A & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
A & tQ1 & 6 & I6 & $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
B & tS1 & 2 & I2 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
B & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
B & tQ1 & 5 & I5 & $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
B & tQ4 & 7 & I7 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & tS1 & 1 & I1 & $\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$ \\
C & tQ1 & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
C & tQ4 & 6 & I6 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
D & tS1 & 3 & I3 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
D & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
D & tQ1 & 5 & I5 & $\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$ \\
D & tQ4 & 6 & I6 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
E & tS1 & 2 & I2 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
E & tQ1 & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
E & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
E & tQ4 & 5 & I5 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
F & tS1 & 1 & I1 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$ \\
F & tQ1 & 2 & I2 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
F & tQ4 & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
F & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$ \\
G & tQ1 & 2 & I2 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$ \\
G & tS1 & 3 & I3 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
G & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
G & tQ4 & 5 & I5 & $\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$ \\
H & tS1 & 1 & I1 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$ \\
H & tS4 & 4 & I4 & $\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$ \\
H & tQ1 & 6 & I6 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
H & tQ4 & 7 & I7 & $\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$ \\
\end{longtable}
```
