# VoltageEdge 到图 3 关键事件映射

图 3 只明确标注每个模式的四个关键开通事件。互补管开通和关断动作保留为 inferred。
图 3 的关键事件顺序按周期循环理解；由于本程序固定以 `v1:0->-1` 为 `edge_0`，部分模式的最后一个图 3 事件会出现在本程序周期起点之前，并在下一周期闭合。

## Mode A

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `0->+1` | `I1` | `tQ4; Q3_off` | `tQ4` | confirmed |
| 2 | `+1->0` | `I2` | `tQ3; Q4_off` | `none` | inferred |
| 3 | `-1->0` | `I3` | `tS1; S2_off` | `tS1` | confirmed |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `0->-1` | `I5` | `tQ2; Q1_off` | `none` | inferred |
| 6 | `-1->0` | `I6` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 7 | `+1->0` | `I7` | `tS3; S4_off` | `none` | inferred |

## Mode B

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `+1->0` | `I1` | `tQ3; Q4_off` | `none` | inferred |
| 2 | `-1->0` | `I2` | `tS1; S2_off` | `tS1` | confirmed |
| 3 | `0->-1` | `I3` | `tQ2; Q1_off` | `none` | inferred |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `-1->0` | `I5` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 6 | `+1->0` | `I6` | `tS3; S4_off` | `none` | inferred |
| 7 | `0->+1` | `I7` | `tQ4; Q3_off` | `tQ4` | confirmed |

## Mode C

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `-1->0` | `I1` | `tS1; S2_off` | `tS1` | confirmed |
| 2 | `0->-1` | `I2` | `tQ2; Q1_off` | `none` | inferred |
| 3 | `-1->0` | `I3` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `+1->0` | `I5` | `tS3; S4_off` | `none` | inferred |
| 6 | `0->+1` | `I6` | `tQ4; Q3_off` | `tQ4` | confirmed |
| 7 | `+1->0` | `I7` | `tQ3; Q4_off` | `none` | inferred |

## Mode D

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `+1->0` | `I1` | `tQ3; Q4_off` | `none` | inferred |
| 2 | `0->-1` | `I2` | `tQ2; Q1_off` | `none` | inferred |
| 3 | `-1->0` | `I3` | `tS1; S2_off` | `tS1` | confirmed |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `-1->0` | `I5` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 6 | `0->+1` | `I6` | `tQ4; Q3_off` | `tQ4` | confirmed |
| 7 | `+1->0` | `I7` | `tS3; S4_off` | `none` | inferred |

## Mode E

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `0->-1` | `I1` | `tQ2; Q1_off` | `none` | inferred |
| 2 | `-1->0` | `I2` | `tS1; S2_off` | `tS1` | confirmed |
| 3 | `-1->0` | `I3` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `0->+1` | `I5` | `tQ4; Q3_off` | `tQ4` | confirmed |
| 6 | `+1->0` | `I6` | `tS3; S4_off` | `none` | inferred |
| 7 | `+1->0` | `I7` | `tQ3; Q4_off` | `none` | inferred |

## Mode F

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `-1->0` | `I1` | `tS1; S2_off` | `tS1` | confirmed |
| 2 | `-1->0` | `I2` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 3 | `0->+1` | `I3` | `tQ4; Q3_off` | `tQ4` | confirmed |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `+1->0` | `I5` | `tS3; S4_off` | `none` | inferred |
| 6 | `+1->0` | `I6` | `tQ3; Q4_off` | `none` | inferred |
| 7 | `0->-1` | `I7` | `tQ2; Q1_off` | `none` | inferred |

## Mode G

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `0->-1` | `I1` | `tQ2; Q1_off` | `none` | inferred |
| 2 | `-1->0` | `I2` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 3 | `-1->0` | `I3` | `tS1; S2_off` | `tS1` | confirmed |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `0->+1` | `I5` | `tQ4; Q3_off` | `tQ4` | confirmed |
| 6 | `+1->0` | `I6` | `tQ3; Q4_off` | `none` | inferred |
| 7 | `+1->0` | `I7` | `tS3; S4_off` | `none` | inferred |

## Mode H

| edge | transition | edge current | candidates | confirmed | confidence |
|---:|---|---|---|---|---|
| 0 | `0->-1` | `I0` | `tS2; S1_off` | `none` | inferred |
| 1 | `-1->0` | `I1` | `tS1; S2_off` | `tS1` | confirmed |
| 2 | `+1->0` | `I2` | `tQ3; Q4_off` | `none` | inferred |
| 3 | `0->-1` | `I3` | `tQ2; Q1_off` | `none` | inferred |
| 4 | `0->+1` | `I4` | `tS4; S3_off` | `tS4` | confirmed |
| 5 | `+1->0` | `I5` | `tS3; S4_off` | `none` | inferred |
| 6 | `-1->0` | `I6` | `tQ1; Q2_off` | `tQ1` | confirmed |
| 7 | `0->+1` | `I7` | `tQ4; Q3_off` | `tQ4` | confirmed |

## 人工复核

- 确认图 3 未标注的互补管开通事件命名。
- 确认是否按理想互补将关断动作与 VoltageEdge 视为同一时刻。
- 确认死区存在时，开通/关断电流采用死区前、死区后还是换流过程中的电流。
