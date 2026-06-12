# A-H 完整周期 VoltageSegment

统一采用 physical 定义：`vL=v1_state*V1-v2_state*n*V2`，`Ts=2*Th=1/fs`。
以下边沿名称仅描述桥输出电压变化，不映射具体开关管 on/off。

生成依据：原边固定电压边沿、由 D/G 验证得到的副边电压边沿表达式、参考论文图 3 的模式排列，以及表 A1 全约束域符号排序。

## Mode A

- 约束：`1 + (D2 - D1)/2 <= phi <= 1 + (D1 - D2)/2`
- 起始段状态：`(-1, 0)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 0) -> (-1, 0)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | secondary | `(-1, 0) -> (-1, 1)` | `(D1 - D2 + 2*phi - 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 2 | secondary | `(-1, 1) -> (-1, 0)` | `(D1 + D2 + 2*phi - 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 3 | primary | `(-1, 0) -> (0, 0)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 4 | primary | `(0, 0) -> (1, 0)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | secondary | `(1, 0) -> (1, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 6 | secondary | `(1, -1) -> (1, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 7 | primary | `(1, 0) -> (0, 0)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 0) -> (-1, 0)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | A_voltage_edge_0 -> A_voltage_edge_1 | `(D1 - D2 + 2*phi - 2)/(4*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 2 | A_voltage_edge_1 -> A_voltage_edge_2 | `D2/(2*fs)` | -1 | 1 | `-V1 - V2*n` | `(-V1 - V2*n)/L` | True |
| 3 | A_voltage_edge_2 -> A_voltage_edge_3 | `(D1 - D2 - 2*phi + 2)/(4*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 4 | A_voltage_edge_3 -> A_voltage_edge_4 | `-(D1 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |
| 5 | A_voltage_edge_4 -> A_voltage_edge_5 | `(D1 - D2 + 2*phi - 2)/(4*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 6 | A_voltage_edge_5 -> A_voltage_edge_6 | `D2/(2*fs)` | 1 | -1 | `V1 + V2*n` | `(V1 + V2*n)/L` | True |
| 7 | A_voltage_edge_6 -> A_voltage_edge_7 | `(D1 - D2 - 2*phi + 2)/(4*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 8 | A_voltage_edge_7 -> A_period_boundary | `-(D1 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |

## Mode B

- 约束：`(D1 + D2)/2 <= phi <= 1 + (D2 - D1)/2 & 1 - (D1 + D2)/2 <= phi <= 1 + (D1 - D2)/2`
- 起始段状态：`(-1, 1)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 1) -> (-1, 1)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | secondary | `(-1, 1) -> (-1, 0)` | `(D1 + D2 + 2*phi - 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 2 | primary | `(-1, 0) -> (0, 0)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 3 | secondary | `(0, 0) -> (0, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 4 | primary | `(0, -1) -> (1, -1)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | secondary | `(1, -1) -> (1, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 6 | primary | `(1, 0) -> (0, 0)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 7 | secondary | `(0, 0) -> (0, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 1) -> (-1, 1)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | B_voltage_edge_0 -> B_voltage_edge_1 | `(D1 + D2 + 2*phi - 2)/(4*fs)` | -1 | 1 | `-V1 - V2*n` | `(-V1 - V2*n)/L` | True |
| 2 | B_voltage_edge_1 -> B_voltage_edge_2 | `(D1 - D2 - 2*phi + 2)/(4*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 3 | B_voltage_edge_2 -> B_voltage_edge_3 | `-(D1 + D2 - 2*phi)/(4*fs)` | 0 | 0 | `0` | `0` | True |
| 4 | B_voltage_edge_3 -> B_voltage_edge_4 | `-(D1 - D2 + 2*phi - 2)/(4*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 5 | B_voltage_edge_4 -> B_voltage_edge_5 | `(D1 + D2 + 2*phi - 2)/(4*fs)` | 1 | -1 | `V1 + V2*n` | `(V1 + V2*n)/L` | True |
| 6 | B_voltage_edge_5 -> B_voltage_edge_6 | `(D1 - D2 - 2*phi + 2)/(4*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 7 | B_voltage_edge_6 -> B_voltage_edge_7 | `-(D1 + D2 - 2*phi)/(4*fs)` | 0 | 0 | `0` | `0` | True |
| 8 | B_voltage_edge_7 -> B_period_boundary | `-(D1 - D2 + 2*phi - 2)/(4*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |

## Mode C

- 约束：`(D1 + D2)/2 <= phi <= 1 - (D1 + D2)/2`
- 起始段状态：`(-1, 0)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 0) -> (-1, 0)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | primary | `(-1, 0) -> (0, 0)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 2 | secondary | `(0, 0) -> (0, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 3 | secondary | `(0, -1) -> (0, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 4 | primary | `(0, 0) -> (1, 0)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | primary | `(1, 0) -> (0, 0)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 6 | secondary | `(0, 0) -> (0, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 7 | secondary | `(0, 1) -> (0, 0)` | `(D1 + D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 0) -> (-1, 0)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | C_voltage_edge_0 -> C_voltage_edge_1 | `D1/(2*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 2 | C_voltage_edge_1 -> C_voltage_edge_2 | `-(D1 + D2 - 2*phi)/(4*fs)` | 0 | 0 | `0` | `0` | True |
| 3 | C_voltage_edge_2 -> C_voltage_edge_3 | `D2/(2*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 4 | C_voltage_edge_3 -> C_voltage_edge_4 | `-(D1 + D2 + 2*phi - 2)/(4*fs)` | 0 | 0 | `0` | `0` | True |
| 5 | C_voltage_edge_4 -> C_voltage_edge_5 | `D1/(2*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 6 | C_voltage_edge_5 -> C_voltage_edge_6 | `-(D1 + D2 - 2*phi)/(4*fs)` | 0 | 0 | `0` | `0` | True |
| 7 | C_voltage_edge_6 -> C_voltage_edge_7 | `D2/(2*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |
| 8 | C_voltage_edge_7 -> C_period_boundary | `-(D1 + D2 + 2*phi - 2)/(4*fs)` | 0 | 0 | `0` | `0` | True |

## Mode D

- 约束：`1 - (D1 + D2)/2 <= phi <= (D1 + D2)/2`
- 起始段状态：`(-1, 1)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 1) -> (-1, 1)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | secondary | `(-1, 1) -> (-1, 0)` | `(D1 + D2 + 2*phi - 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 2 | secondary | `(-1, 0) -> (-1, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 3 | primary | `(-1, -1) -> (0, -1)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 4 | primary | `(0, -1) -> (1, -1)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | secondary | `(1, -1) -> (1, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 6 | secondary | `(1, 0) -> (1, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 7 | primary | `(1, 1) -> (0, 1)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 1) -> (-1, 1)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | D_voltage_edge_0 -> D_voltage_edge_1 | `(D1 + D2 + 2*phi - 2)/(4*fs)` | -1 | 1 | `-V1 - V2*n` | `(-V1 - V2*n)/L` | True |
| 2 | D_voltage_edge_1 -> D_voltage_edge_2 | `-(D2 - 1)/(2*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 3 | D_voltage_edge_2 -> D_voltage_edge_3 | `(D1 + D2 - 2*phi)/(4*fs)` | -1 | -1 | `-V1 + V2*n` | `(-V1 + V2*n)/L` | True |
| 4 | D_voltage_edge_3 -> D_voltage_edge_4 | `-(D1 - 1)/(2*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 5 | D_voltage_edge_4 -> D_voltage_edge_5 | `(D1 + D2 + 2*phi - 2)/(4*fs)` | 1 | -1 | `V1 + V2*n` | `(V1 + V2*n)/L` | True |
| 6 | D_voltage_edge_5 -> D_voltage_edge_6 | `-(D2 - 1)/(2*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 7 | D_voltage_edge_6 -> D_voltage_edge_7 | `(D1 + D2 - 2*phi)/(4*fs)` | 1 | 1 | `V1 - V2*n` | `(V1 - V2*n)/L` | True |
| 8 | D_voltage_edge_7 -> D_period_boundary | `-(D1 - 1)/(2*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |

## Mode E

- 约束：`(D1 - D2)/2 <= phi <= 1 - (D1 + D2)/2 & (D2 - D1)/2 <= phi <= (D1 + D2)/2`
- 起始段状态：`(-1, 0)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 0) -> (-1, 0)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | secondary | `(-1, 0) -> (-1, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 2 | primary | `(-1, -1) -> (0, -1)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 3 | secondary | `(0, -1) -> (0, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 4 | primary | `(0, 0) -> (1, 0)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | secondary | `(1, 0) -> (1, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 6 | primary | `(1, 1) -> (0, 1)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 7 | secondary | `(0, 1) -> (0, 0)` | `(D1 + D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 0) -> (-1, 0)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | E_voltage_edge_0 -> E_voltage_edge_1 | `(D1 - D2 + 2*phi)/(4*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 2 | E_voltage_edge_1 -> E_voltage_edge_2 | `(D1 + D2 - 2*phi)/(4*fs)` | -1 | -1 | `-V1 + V2*n` | `(-V1 + V2*n)/L` | True |
| 3 | E_voltage_edge_2 -> E_voltage_edge_3 | `-(D1 - D2 - 2*phi)/(4*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 4 | E_voltage_edge_3 -> E_voltage_edge_4 | `-(D1 + D2 + 2*phi - 2)/(4*fs)` | 0 | 0 | `0` | `0` | True |
| 5 | E_voltage_edge_4 -> E_voltage_edge_5 | `(D1 - D2 + 2*phi)/(4*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 6 | E_voltage_edge_5 -> E_voltage_edge_6 | `(D1 + D2 - 2*phi)/(4*fs)` | 1 | 1 | `V1 - V2*n` | `(V1 - V2*n)/L` | True |
| 7 | E_voltage_edge_6 -> E_voltage_edge_7 | `-(D1 - D2 - 2*phi)/(4*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |
| 8 | E_voltage_edge_7 -> E_period_boundary | `-(D1 + D2 + 2*phi - 2)/(4*fs)` | 0 | 0 | `0` | `0` | True |

## Mode F

- 约束：`(D1 - D2)/2 <= phi <= (D2 - D1)/2`
- 起始段状态：`(-1, -1)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, -1) -> (-1, -1)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | primary | `(-1, -1) -> (0, -1)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 2 | secondary | `(0, -1) -> (0, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 3 | secondary | `(0, 0) -> (0, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 4 | primary | `(0, 1) -> (1, 1)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | primary | `(1, 1) -> (0, 1)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 6 | secondary | `(0, 1) -> (0, 0)` | `(D1 + D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 7 | secondary | `(0, 0) -> (0, -1)` | `(D1 - D2 + 2*phi + 4)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 8 | period_boundary | `(0, -1) -> (-1, -1)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | F_voltage_edge_0 -> F_voltage_edge_1 | `D1/(2*fs)` | -1 | -1 | `-V1 + V2*n` | `(-V1 + V2*n)/L` | True |
| 2 | F_voltage_edge_1 -> F_voltage_edge_2 | `-(D1 - D2 - 2*phi)/(4*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 3 | F_voltage_edge_2 -> F_voltage_edge_3 | `-(D2 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |
| 4 | F_voltage_edge_3 -> F_voltage_edge_4 | `-(D1 - D2 + 2*phi)/(4*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |
| 5 | F_voltage_edge_4 -> F_voltage_edge_5 | `D1/(2*fs)` | 1 | 1 | `V1 - V2*n` | `(V1 - V2*n)/L` | True |
| 6 | F_voltage_edge_5 -> F_voltage_edge_6 | `-(D1 - D2 - 2*phi)/(4*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |
| 7 | F_voltage_edge_6 -> F_voltage_edge_7 | `-(D2 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |
| 8 | F_voltage_edge_7 -> F_period_boundary | `-(D1 - D2 + 2*phi)/(4*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |

## Mode G

- 约束：`(D2 - D1)/2 <= phi <= (D1 - D2)/2`
- 起始段状态：`(-1, 0)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 0) -> (-1, 0)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | secondary | `(-1, 0) -> (-1, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 2 | secondary | `(-1, -1) -> (-1, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 3 | primary | `(-1, 0) -> (0, 0)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 4 | primary | `(0, 0) -> (1, 0)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | secondary | `(1, 0) -> (1, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 6 | secondary | `(1, 1) -> (1, 0)` | `(D1 + D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 7 | primary | `(1, 0) -> (0, 0)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 0) -> (-1, 0)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | G_voltage_edge_0 -> G_voltage_edge_1 | `(D1 - D2 + 2*phi)/(4*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 2 | G_voltage_edge_1 -> G_voltage_edge_2 | `D2/(2*fs)` | -1 | -1 | `-V1 + V2*n` | `(-V1 + V2*n)/L` | True |
| 3 | G_voltage_edge_2 -> G_voltage_edge_3 | `(D1 - D2 - 2*phi)/(4*fs)` | -1 | 0 | `-V1` | `-V1/L` | True |
| 4 | G_voltage_edge_3 -> G_voltage_edge_4 | `-(D1 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |
| 5 | G_voltage_edge_4 -> G_voltage_edge_5 | `(D1 - D2 + 2*phi)/(4*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 6 | G_voltage_edge_5 -> G_voltage_edge_6 | `D2/(2*fs)` | 1 | 1 | `V1 - V2*n` | `(V1 - V2*n)/L` | True |
| 7 | G_voltage_edge_6 -> G_voltage_edge_7 | `(D1 - D2 - 2*phi)/(4*fs)` | 1 | 0 | `V1` | `V1/L` | True |
| 8 | G_voltage_edge_7 -> G_period_boundary | `-(D1 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |

## Mode H

- 约束：`1 + (D1 - D2)/2 <= phi <= 1 + (D2 - D1)/2`
- 起始段状态：`(-1, 1)`
- 来源：参考论文图3 + 表A1；D/G 另经 legacy 人工参数回归验证

### VoltageEdge

| index | bridge | from -> to | cumulative_time_expr | note |
|---:|---|---|---|---|
| 0 | primary | `(0, 1) -> (-1, 1)` | `0` | 电压边沿类型: p_neg_on；不映射具体开关事件。 |
| 1 | primary | `(-1, 1) -> (0, 1)` | `D1/(2*fs)` | 电压边沿类型: p_neg_off；不映射具体开关事件。 |
| 2 | secondary | `(0, 1) -> (0, 0)` | `(D1 + D2 + 2*phi - 2)/(4*fs)` | 电压边沿类型: s_pos_off；不映射具体开关事件。 |
| 3 | secondary | `(0, 0) -> (0, -1)` | `(D1 - D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_on；不映射具体开关事件。 |
| 4 | primary | `(0, -1) -> (1, -1)` | `1/(2*fs)` | 电压边沿类型: p_pos_on；不映射具体开关事件。 |
| 5 | primary | `(1, -1) -> (0, -1)` | `(D1 + 1)/(2*fs)` | 电压边沿类型: p_pos_off；不映射具体开关事件。 |
| 6 | secondary | `(0, -1) -> (0, 0)` | `(D1 + D2 + 2*phi)/(4*fs)` | 电压边沿类型: s_neg_off；不映射具体开关事件。 |
| 7 | secondary | `(0, 0) -> (0, 1)` | `(D1 - D2 + 2*phi + 2)/(4*fs)` | 电压边沿类型: s_pos_on；不映射具体开关事件。 |
| 8 | period_boundary | `(0, 1) -> (-1, 1)` | `1/fs` | 与下一周期 t=0 的首个电压边沿相接。 |

### VoltageSegment

| seg | start -> end | duration_expr | v1 | v2 | vL_expr | slope_expr | zero possible |
|---:|---|---|---:|---:|---|---|---|
| 1 | H_voltage_edge_0 -> H_voltage_edge_1 | `D1/(2*fs)` | -1 | 1 | `-V1 - V2*n` | `(-V1 - V2*n)/L` | True |
| 2 | H_voltage_edge_1 -> H_voltage_edge_2 | `-(D1 - D2 - 2*phi + 2)/(4*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |
| 3 | H_voltage_edge_2 -> H_voltage_edge_3 | `-(D2 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |
| 4 | H_voltage_edge_3 -> H_voltage_edge_4 | `-(D1 - D2 + 2*phi - 2)/(4*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 5 | H_voltage_edge_4 -> H_voltage_edge_5 | `D1/(2*fs)` | 1 | -1 | `V1 + V2*n` | `(V1 + V2*n)/L` | True |
| 6 | H_voltage_edge_5 -> H_voltage_edge_6 | `-(D1 - D2 - 2*phi + 2)/(4*fs)` | 0 | -1 | `V2*n` | `V2*n/L` | True |
| 7 | H_voltage_edge_6 -> H_voltage_edge_7 | `-(D2 - 1)/(2*fs)` | 0 | 0 | `0` | `0` | True |
| 8 | H_voltage_edge_7 -> H_period_boundary | `-(D1 - D2 + 2*phi - 2)/(4*fs)` | 0 | 1 | `-V2*n` | `-V2*n/L` | True |

## TODO

- D/G 已与 legacy 逐段回归一致。
- A/B/C/E/F/H 已通过图 3 + 表 A1 的符号排列与非负性校验，但仍建议人工对照图 3 复核电压波形视觉顺序。
- VoltageEdge 暂不映射为具体开关事件。
