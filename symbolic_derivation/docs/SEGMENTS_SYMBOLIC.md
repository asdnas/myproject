# 自动符号分段状态

当前主分段层改为 `voltage_segments.py`，已实现：

- `VoltageEdge` 和 `VoltageSegment` 数据结构；
- physical 电压定义与 legacy 副边符号转换；
- 从 D/G legacy 人工配置恢复完整周期 8 段；
- 统一 `vL = v1_state*V1 - v2_state*n*V2` 与斜率。

A-H 均已由图 3 电压波形排列和表 A1 约束生成完整周期 8 段。D/G 另与 legacy
反推结果逐段回归一致。A/B/C/E/F/H 仍建议人工对照图 3 做视觉复核，但符号排序、
总周期和非负性校验均已通过。
