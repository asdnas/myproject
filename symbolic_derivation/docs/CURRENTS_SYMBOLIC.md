# 符号电流推导状态

`current_solver.py` 已实现 A-H 通用递推和与 legacy 一致的面积约束：

`I[k+1] = I[k] + slope[k]*duration[k]`

`sum((I[k]+I[k+1])*duration[k]/2) = 0`

目前 A-H 均已成功求出 `I0...I8` 和 8 段面积，并全部满足：

- `sum(dt)=Ts`
- `sum(k*dt)=0`
- `I8-I0=0`
- 面积约束代回后为 `0`

D/G 与旧 `engine.py` 按相同物理边界循环对齐后，9 个边界电流逐项一致。
详细公式见 `AH_CURRENTS_SYMBOLIC.md`，检查见 `AH_CURRENT_CHECKS.md`。
