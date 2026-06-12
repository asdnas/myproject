# D/G Legacy 电流对比

旧程序周期起点与新 VoltageSegment 周期起点不同。新周期从旧配置第 5 段开始，因此必须按同一物理边界循环对齐，不能直接比较同名下标。

| new current | aligned legacy current |
|---|---|
| I0 | legacy_I4 |
| I1 | legacy_I5 |
| I2 | legacy_I6 |
| I3 | legacy_I7 |
| I4 | legacy_I8 |
| I5 | legacy_I1 |
| I6 | legacy_I2 |
| I7 | legacy_I3 |
| I8 | legacy_I4 |

## Mode D

- 全部逐项一致：`True`

| new current | aligned legacy current | difference |
|---|---|---|
| I0 | legacy_I4 | `0` |
| I1 | legacy_I5 | `0` |
| I2 | legacy_I6 | `0` |
| I3 | legacy_I7 | `0` |
| I4 | legacy_I8 | `0` |
| I5 | legacy_I1 | `0` |
| I6 | legacy_I2 | `0` |
| I7 | legacy_I3 | `0` |
| I8 | legacy_I4 | `0` |

## Mode G

- 全部逐项一致：`True`

| new current | aligned legacy current | difference |
|---|---|---|
| I0 | legacy_I4 | `0` |
| I1 | legacy_I5 | `0` |
| I2 | legacy_I6 | `0` |
| I3 | legacy_I7 | `0` |
| I4 | legacy_I8 | `0` |
| I5 | legacy_I1 | `0` |
| I6 | legacy_I2 | `0` |
| I7 | legacy_I3 | `0` |
| I8 | legacy_I4 | `0` |
