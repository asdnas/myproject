# Traditional TPS 候选关断电流符号公式

图 3 未直接标注关断事件，因此当前全部关断映射均为 `inferred`。
`turn_off_index_expr=Abs(current_expr)` 仅为形式化指标，后续数值代入后可用于比较。

## Mode A

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 1 | Q3_off | `(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | inferred |
| 2 | Q4_off | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| 3 | S2_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 5 | Q1_off | `(-D2*V1 - D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | inferred |
| 6 | Q2_off | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| 7 | S4_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |

## Mode B

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| 1 | Q4_off | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| 2 | S2_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 3 | Q1_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| 5 | Q2_off | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| 6 | S4_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 7 | Q3_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |

## Mode C

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 1 | S2_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 2 | Q1_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 3 | Q2_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 5 | S4_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 6 | Q3_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 7 | Q4_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode D

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| 1 | Q4_off | `(-D2*V1 - D2*V2*n - 2*V1*phi + 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| 2 | Q1_off | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 3 | S2_off | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| 5 | Q2_off | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `Abs(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | inferred |
| 6 | Q3_off | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 7 | S4_off | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |

## Mode E

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 1 | Q1_off | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 2 | S2_off | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 3 | Q2_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 5 | Q3_off | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 6 | S4_off | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 7 | Q4_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode F

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 - D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `Abs(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 1 | S2_off | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 2 | Q2_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 3 | Q3_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `Abs(-D1*V1 + D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 5 | S4_off | `(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | `Abs(D1*V1 - D1*V2*n + 2*V2*n*phi)/(4*L*fs)` | inferred |
| 6 | Q4_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 7 | Q1_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode G

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 1 | Q1_off | `(D2*V1 - D2*V2*n - 2*V1*phi)/(4*L*fs)` | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 2 | Q2_off | `(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | `Abs(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 3 | S2_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |
| 5 | Q3_off | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `Abs(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 6 | Q4_off | `(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | `Abs(D2*V1 - D2*V2*n + 2*V1*phi)/(4*L*fs)` | inferred |
| 7 | S4_off | `(D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 - D2*V2*n)/(4*L*fs)` | inferred |

## Mode H

| edge | candidate off event | current expression | turn-off index | confidence |
|---:|---|---|---|---|
| 0 | S1_off | `(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| 1 | S2_off | `(-D1*V1 - D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | inferred |
| 2 | Q4_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 3 | Q1_off | `(-D1*V1 - D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 4 | S3_off | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n + 2*V2*n*phi - 2*V2*n)/(4*L*fs)` | inferred |
| 5 | S4_off | `(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | inferred |
| 6 | Q2_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |
| 7 | Q3_off | `(D1*V1 + D2*V2*n)/(4*L*fs)` | `Abs(D1*V1 + D2*V2*n)/(4*L*fs)` | inferred |

