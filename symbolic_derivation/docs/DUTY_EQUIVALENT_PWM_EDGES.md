# Duty-equivalent 理想 PWM 边沿

当前使用用户接线表，忽略 dead-band 延时。下表先列 `case_source_actual`：

| switch | 理想 on 边沿 | 理想 off 边沿 |
|---|---|---|
| S1 | `Mod(Ts-D1*Ts/4,Ts)` | `D1*Ts/4` |
| S2 | `D1*Ts/4` | `Mod(Ts-D1*Ts/4,Ts)` |
| S3 | `Ts/2-D1*Ts/4` | `Ts/2+D1*Ts/4` |
| S4 | `Ts/2+D1*Ts/4` | `Ts/2-D1*Ts/4` |
| Q1 | `Mod(phi*Ts/3+Ts-D2*Ts/4,Ts)` | `Mod(phi*Ts/3+D2*Ts/4,Ts)` |
| Q2 | `Mod(phi*Ts/3+D2*Ts/4,Ts)` | `Mod(phi*Ts/3+Ts-D2*Ts/4,Ts)` |
| Q3 | `Mod(phi*Ts/3+Ts/2-D2*Ts/4,Ts)` | `Mod(phi*Ts/3+Ts/2+D2*Ts/4,Ts)` |
| Q4 | `Mod(phi*Ts/3+Ts/2+D2*Ts/4,Ts)` | `Mod(phi*Ts/3+Ts/2-D2*Ts/4,Ts)` |

`case_corrected_expected` 将所有副边表达式中的 `+phi*Ts/3` 改为 `+phi*Ts/2`。

```text
python -m symbolic_derivation.duty_equivalent_edges --review-source
```
