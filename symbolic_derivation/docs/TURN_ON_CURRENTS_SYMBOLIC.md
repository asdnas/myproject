# Traditional TPS 开通电流符号公式

每个模式有 4 个图 3 confirmed 关键开通事件，以及 4 个由 H 桥规则 inferred 的互补管开通事件。

## Mode A

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 1 | tQ4 | confirmed | `(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| 2 | tQ3 | inferred | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| 3 | tS1 | confirmed | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 5 | tQ2 | inferred | `(-D2*V1 - D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| 6 | tQ1 | confirmed | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| 7 | tS3 | inferred | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |

## Mode B

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| 1 | tQ3 | inferred | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| 2 | tS1 | confirmed | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 3 | tQ2 | inferred | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| 5 | tQ1 | confirmed | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| 6 | tS3 | inferred | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 7 | tQ4 | confirmed | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |

## Mode C

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 1 | tS1 | confirmed | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 2 | tQ2 | inferred | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 3 | tQ1 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 5 | tS3 | inferred | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 6 | tQ4 | confirmed | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 7 | tQ3 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

## Mode D

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| 1 | tQ3 | inferred | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `$\frac{- D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi + 2 V_{1}}{4 L fs}$` |
| 2 | tQ2 | inferred | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| 3 | tS1 | confirmed | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| 5 | tQ1 | confirmed | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `$\frac{D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi - 2 V_{1}}{4 L fs}$` |
| 6 | tQ4 | confirmed | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| 7 | tS3 | inferred | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |

## Mode E

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 1 | tQ2 | inferred | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| 2 | tS1 | confirmed | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| 3 | tQ1 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 5 | tQ4 | confirmed | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| 6 | tS3 | inferred | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| 7 | tQ3 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

## Mode F

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 - D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| 1 | tS1 | confirmed | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi}{4 L fs}$` |
| 2 | tQ1 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 3 | tQ4 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| 5 | tS3 | inferred | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi}{4 L fs}$` |
| 6 | tQ3 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 7 | tQ2 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

## Mode G

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 1 | tQ2 | inferred | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| 2 | tQ1 | confirmed | `(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n - 2 V_{1} \phi}{4 L fs}$` |
| 3 | tS1 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 5 | tQ4 | confirmed | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{- D_{2} V_{1} + D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| 6 | tQ3 | inferred | `(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | `$\frac{D_{2} V_{1} - D_{2} V_{2} n + 2 V_{1} \phi}{4 L fs}$` |
| 7 | tS3 | inferred | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |

## Mode H

| edge | event | confidence | current expression | LaTeX |
|---:|---|---|---|---|
| 0 | tS2 | inferred | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| 1 | tS1 | confirmed | `(-D1*V1 - D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n + 2 V_{2} n \phi - 2 V_{2} n}{4 L fs}$` |
| 2 | tQ3 | inferred | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 3 | tQ2 | inferred | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{2} V_{2} n}{4 L fs}$` |
| 4 | tS4 | confirmed | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `$\frac{- D_{1} V_{1} - D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| 5 | tS3 | inferred | `(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{1} V_{2} n - 2 V_{2} n \phi + 2 V_{2} n}{4 L fs}$` |
| 6 | tQ1 | confirmed | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |
| 7 | tQ4 | confirmed | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `$\frac{D_{1} V_{1} + D_{2} V_{2} n}{4 L fs}$` |

## D/G 论文表 1 核对

- Mode D: tS1 差值=`0`, tS4 差值=`0`, tQ1 差值=`0`, tQ4 差值=`0`
- Mode G: tQ1 差值=`0`, tS1 差值=`0`, tS4 差值=`0`, tQ4 差值=`0`

图 3 未标注的 inferred 开通项已同时写入 `switch_event_mapping_todo.csv`。
