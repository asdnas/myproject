# Duty-equivalent D/G VoltageSegment

以下先记录 `case_source_actual`：正 `phi` 表示副边滞后，`phase_time=phi*Ts/3`。全部忽略死区。

## D 模式候选

D 候选具有 8 个状态段且总时间为 Ts，但第 1/5 段在原 TPS-D 约束域内可能为负，因此不是整个 D 域上的有效固定顺序模型。需要重新划分 duty-equivalent D 子模式。

| seg | duration | v1 | v2 | vL | slope | 全 D 域非负 |
|---:|---|---:|---:|---|---|---|
| 1 | `(3D1+3D2+4phi-6)/(12fs)` | -1 | +1 | `-V1-nV2` | `(-V1-nV2)/L` | 否 |
| 2 | `(1-D2)/(2fs)` | -1 | 0 | `-V1` | `-V1/L` | 是 |
| 3 | `(D1/4+D2/4-phi/3)/fs` | -1 | -1 | `-V1+nV2` | `(-V1+nV2)/L` | 是 |
| 4 | `(1-D1)/(2fs)` | 0 | -1 | `nV2` | `nV2/L` | 是 |
| 5 | `(3D1+3D2+4phi-6)/(12fs)` | +1 | -1 | `V1+nV2` | `(V1+nV2)/L` | 否 |
| 6 | `(1-D2)/(2fs)` | +1 | 0 | `V1` | `V1/L` | 是 |
| 7 | `(D1/4+D2/4-phi/3)/fs` | +1 | +1 | `V1-nV2` | `(V1-nV2)/L` | 是 |
| 8 | `(1-D1)/(2fs)` | 0 | +1 | `-nV2` | `-nV2/L` | 是 |

形式候选仍满足 `sum(dt)=Ts`、`sum(k*dt)=0`、`I8-I0=0`、面积约束为 0，但不能作为全 D 域物理解。

## G 模式

G 在原表 A1 约束域内保持固定 8 段，所有持续时间非负。

| seg | duration | v1 | v2 | vL | slope |
|---:|---|---:|---:|---|---|
| 1 | `(D1/4-D2/4+phi/3)/fs` | -1 | 0 | `-V1` | `-V1/L` |
| 2 | `D2/(2fs)` | -1 | -1 | `-V1+nV2` | `(-V1+nV2)/L` |
| 3 | `(D1/4-D2/4-phi/3)/fs` | -1 | 0 | `-V1` | `-V1/L` |
| 4 | `(1-D1)/(2fs)` | 0 | 0 | `0` | `0` |
| 5 | `(D1/4-D2/4+phi/3)/fs` | +1 | 0 | `V1` | `V1/L` |
| 6 | `D2/(2fs)` | +1 | +1 | `V1-nV2` | `(V1-nV2)/L` |
| 7 | `(D1/4-D2/4-phi/3)/fs` | +1 | 0 | `V1` | `V1/L` |
| 8 | `(1-D1)/(2fs)` | 0 | 0 | `0` | `0` |

G 满足 `sum(dt)=Ts`、`sum(k*dt)=0`、`I8-I0=0`、面积约束为 0。

## case_corrected_expected

修正为 `phase_time=phi*Ts/2=phi*Th` 后：

- D/G 均恢复为有效固定顺序 8 段；
- D/G duration、状态、vL 和 slope 均与 traditional TPS 逐段一致；
- D 模式不再存在负 duration。
