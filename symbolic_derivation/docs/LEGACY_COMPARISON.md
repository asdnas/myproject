# Legacy 对比

已确认新 `current_solver.py` 可读取整理后的 D/G legacy 人工配置，并保留旧程序的
`vL=v1*V1+v2*n*V2` 符号约定进行精确复算。

同时已确认 `v2_physical=-v2_legacy` 后，D/G physical VoltageSegment 的每段斜率
与对应 legacy 分段严格一致。physical 周期为了满足 `t=0` 时 `v1=-1` 的规则进行了
循环旋转，因此边界电流下标会随周期起点改变，不能直接按相同 `I0` 下标比较。

A-H VoltageSegment 已完成；D/G 新电流与旧 `engine.py` 电流按相同物理
边界循环对齐后，`I0...I8` 九个边界值逐项差值均为零。详见
`LEGACY_CURRENT_COMPARISON.md`。
