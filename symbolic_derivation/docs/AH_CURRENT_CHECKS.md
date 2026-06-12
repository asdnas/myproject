# A-H 电流符号检查

所有检查均为 SymPy 符号化简结果，没有代入数值点。

| mode | total_time-Ts | sum(k*dt) | I8-I0 | area after I0 substitution | solve status |
|---|---|---|---|---|---|
| A | `0` | `0` | `0` | `0` | success |
| B | `0` | `0` | `0` | `0` | success |
| C | `0` | `0` | `0` | `0` | success |
| D | `0` | `0` | `0` | `0` | success |
| E | `0` | `0` | `0` | `0` | success |
| F | `0` | `0` | `0` | `0` | success |
| G | `0` | `0` | `0` | `0` | success |
| H | `0` | `0` | `0` | `0` | success |

## D/G Legacy 电流回归

新 VoltageSegment 周期从 legacy boundary 4 开始，因此旧电流按物理边界循环对齐为：
`legacy_I4,I5,I6,I7,I8,I1,I2,I3,I4`。

- Mode D: 9 个边界电流逐项一致 = `True`；差值 = `(0, 0, 0, 0, 0, 0, 0, 0, 0)`。
- Mode G: 9 个边界电流逐项一致 = `True`；差值 = `(0, 0, 0, 0, 0, 0, 0, 0, 0)`。

## 结论

- A-H 均成功使用面积约束求解 `I0`。
- A-H 均满足完整周期伏秒平衡与电流周期闭合。
- 当前结果仅是 VoltageEdge 边界电流，未映射具体开关事件。
