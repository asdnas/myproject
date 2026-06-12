# 电压符号约定审查

## 新程序统一定义：physical

原边状态：

- `v1_state=+1` 表示 `+V1`
- `v1_state=0` 表示 `0`
- `v1_state=-1` 表示 `-V1`

副边状态：

- `v2_state=+1` 表示折算到原边后的 `+nV2`
- `v2_state=0` 表示 `0`
- `v2_state=-1` 表示折算到原边后的 `-nV2`

新程序统一使用：

`vL = v1_state*V1 - v2_state*n*V2`

`slope = vL/L`

## Legacy 兼容

旧程序实际使用：

`vL = v1_legacy*V1 + v2_legacy*n*V2`

两套定义之间：

`v1_physical = v1_legacy`

`v2_physical = -v2_legacy`

因此：

`v1_physical*V1 - v2_physical*n*V2`

`= v1_legacy*V1 + v2_legacy*n*V2`

转换在 `voltage_segments.py` 中实现。新 VoltageSegment 只保存 physical 状态；
legacy 原始状态仅用于兼容读取和精确对比。
