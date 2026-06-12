# A-H VoltageSegment 校验

校验不是数值采样。持续时间的最小值和最大值通过表 A1 线性约束多面体顶点求得。
B/E 中 `&` 按“且”加入约束集合。

| mode | segment count | total time = Ts | all duration nonnegative | zero-duration segments | states valid | physical vL valid |
|---|---:|---|---|---|---|---|
| A | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| B | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| C | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| D | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| E | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| F | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| G | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |
| H | 8 | True | True | 1,2,3,4,5,6,7,8 | True | True |

## D/G Legacy 回归

- Mode D: 8 段 duration/state/vL/slope 逐项一致 = `True`。
- Mode G: 8 段 duration/state/vL/slope 逐项一致 = `True`。

## 人工复核需求

- D/G 无需重新确认分段公式，仅需后续确认图 3 标注点映射。
- A/B/C/E/F/H 建议人工对照图 3 复核电压状态视觉顺序；当前符号校验均通过。
- 所有模式的所有段都可能在某个表 A1 模式边界退化为零长度段。
