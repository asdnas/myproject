# Duty-equivalent 与 traditional TPS 对比

## 两种 case

| case | phase count | phase time | 含义 |
|---|---|---|---|
| `case_source_actual` | `Abs(phi)*(2/3)*TBPRD` | `phi*Ts/3` | 当前源码实际行为 |
| `case_corrected_expected` | `Abs(phi)*TBPRD` | `phi*Ts/2=phi*Th` | `fai=phi_paper` 时的理论正确行为 |

两者均取正常功率方向：正 phi 时原边超前、副边滞后。

## Source Actual

当前源码相移比期望少 `phi*Ts/6`。

G 模式状态、vL 和 slope 序列与 TPS 相同，但边沿持续时间和部分电流不同：

- `tS1/tS4` 电流差为 0；
- `tQ1` 电流差为 `+V1*phi/(6Lfs)`；
- `tQ4` 电流差为 `-V1*phi/(6Lfs)`；
- 副边 inferred 关断边界也发生相同量级变化。

D 模式在原 TPS-D 约束域内出现负候选段，说明错误缩放改变了模式边界。

## Corrected Expected

修正为 `phase_time=phi*Th` 后：

- D/G 每个模式均为有效固定顺序 8 段；
- 所有 duration、v1_state、v2_state、vL、slope 与 TPS 逐项一致；
- D/G 所有 `I0...I8` 与 TPS 逐项一致；
- D/G 的 `tS1/tS4/tQ1/tQ4` 开通电流差全部为 0；
- D/G 全部 inferred 理想关断电流差也全部为 0。

因此，在忽略死区的理想模型中，修正 TBPHS 后 duty-equivalent 的完整桥输出电压过程与 traditional TPS 等效，不只是开通过程等效。

## 论文结论

修正 TBPHS 后，可以沿用 traditional TPS 的开通软开关条件。

在当前理想、忽略死区的模型中，关断电流也与 TPS 相同，不能据此声称 duty-equivalent 会改变关断损耗。若要得到关断差异，需要进一步纳入死区、器件延时或不同实际门极边沿机制。
