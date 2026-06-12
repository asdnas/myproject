# D/G Legacy 电压边界恢复

## 恢复规则

1. 使用 `v1_physical=v1_legacy`、`v2_physical=-v2_legacy`。
2. 将 legacy 第 5 段旋转为新周期第 1 段。
3. 此时 D/G 均满足：`t=0` 时 `v1=-1`，经过前三段合计 `D1*Th` 后，原边由
   `-1` 跳变为 `0`。
4. 边界仅按电压变化命名，不映射具体开关管事件。

状态写作 `(v1_state,v2_state)`，均为 physical 定义。

## 模式 D 边界

| 边界 | time | 状态变化 | 跳变桥 | 图 3 对应关系 |
|---|---|---|---|---|
| D_voltage_edge_0 | `0` | `(0,+1)->(-1,+1)` | primary | 周期起点的原边电压跳变；具体开关事件待确认 |
| D_voltage_edge_1 | `((D1+D2)/2+phi-1)Th` | `(-1,+1)->(-1,0)` | secondary | 副边第一次跳变；具体图 3 标注点待确认 |
| D_voltage_edge_2 | `((D1-D2)/2+phi)Th` | `(-1,0)->(-1,-1)` | secondary | 副边第二次跳变；具体图 3 标注点待确认 |
| D_voltage_edge_3 | `D1*Th` | `(-1,-1)->(0,-1)` | primary | 用户确认的 `-V1 -> 0` 跳变 |
| D_voltage_edge_4 | `Th` | `(0,-1)->(+1,-1)` | primary | 原边后续跳变；具体图 3 标注点待确认 |
| D_voltage_edge_5 | `((D1+D2)/2+phi)Th` | `(+1,-1)->(+1,0)` | secondary | 副边跳变；具体图 3 标注点待确认 |
| D_voltage_edge_6 | `(1+(D1-D2)/2+phi)Th` | `(+1,0)->(+1,+1)` | secondary | 副边跳变；具体图 3 标注点待确认 |
| D_voltage_edge_7 | `(D1+1)Th` | `(+1,+1)->(0,+1)` | primary | 原边跳变；具体图 3 标注点待确认 |
| D_period_boundary | `Ts` | `(0,+1)->(-1,+1)` | period boundary | 闭合到下一周期 |

## 模式 G 边界

| 边界 | time | 状态变化 | 跳变桥 | 图 3 对应关系 |
|---|---|---|---|---|
| G_voltage_edge_0 | `0` | `(0,0)->(-1,0)` | primary | 周期起点的原边电压跳变；具体开关事件待确认 |
| G_voltage_edge_1 | `(D1/2-D2/2+phi)Th` | `(-1,0)->(-1,-1)` | secondary | 副边第一次跳变；具体图 3 标注点待确认 |
| G_voltage_edge_2 | `(D1/2+D2/2+phi)Th` | `(-1,-1)->(-1,0)` | secondary | 副边第二次跳变；具体图 3 标注点待确认 |
| G_voltage_edge_3 | `D1*Th` | `(-1,0)->(0,0)` | primary | 用户确认的 `-V1 -> 0` 跳变 |
| G_voltage_edge_4 | `Th` | `(0,0)->(+1,0)` | primary | 原边后续跳变；具体图 3 标注点待确认 |
| G_voltage_edge_5 | `(1+(D1-D2)/2+phi)Th` | `(+1,0)->(+1,+1)` | secondary | 副边跳变；具体图 3 标注点待确认 |
| G_voltage_edge_6 | `(1+(D1+D2)/2+phi)Th` | `(+1,+1)->(+1,0)` | secondary | 副边跳变；具体图 3 标注点待确认 |
| G_voltage_edge_7 | `(D1+2)Th` | `(+1,0)->(0,0)` | primary | 原边跳变；具体图 3 标注点待确认 |
| G_period_boundary | `Ts` | `(0,0)->(-1,0)` | period boundary | 闭合到下一周期 |

## 结论

D/G 的 8 个实际段边界均可判断为仅原边或仅副边电压跳变；没有 `both` 跳变。
模式边界上持续时间可为零，届时相邻单桥跳变可能在同一时刻重合，但仍不应在未验证前
强行合并或命名为具体开关事件。

使用表 A1 的 D/G 全约束域验证后，全部 8 段持续时间均恒非负，且每段都存在取零的
模式边界。
