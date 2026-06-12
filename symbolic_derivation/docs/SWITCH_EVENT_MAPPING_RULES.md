# Traditional TPS 开关事件映射规则

VoltageEdge 边界电流只是桥输出电压发生跳变时的电感电流。要得到具体开关管的开通/关断电流，还需要结合 H 桥导通状态、同桥臂互补关系和论文图 3 标注。

## 基础映射

| bridge | voltage transition | on event | paired off event | on confidence |
|---|---|---|---|---|
| primary | `-1->0` | `tS1` | `S2_off` | confirmed by Fig.3 |
| primary | `0->+1` | `tS4` | `S3_off` | confirmed by Fig.3 |
| primary | `+1->0` | `tS3` | `S4_off` | inferred by H-bridge rule |
| primary | `0->-1` | `tS2` | `S1_off` | inferred by H-bridge rule |
| secondary | `-1->0` | `tQ1` | `Q2_off` | confirmed by Fig.3 |
| secondary | `0->+1` | `tQ4` | `Q3_off` | confirmed by Fig.3 |
| secondary | `+1->0` | `tQ3` | `Q4_off` | inferred by H-bridge rule |
| secondary | `0->-1` | `tQ2` | `Q1_off` | inferred by H-bridge rule |

## 置信度定义

- `confirmed`：图 3 明确标注的 `tS1/tS4/tQ1/tQ4`，且循环顺序与 VoltageEdge 一致。
- `inferred`：由同桥臂互补和电压状态变化推得，但图 3 未直接标注。
- `todo`：现有材料无法确认。当前主要保留死区期间的电流取值约定与关断边界确认。

所有关断事件当前均为 `inferred`。关断指标仅使用 `Abs(current_expr)`，未加入器件模型。
