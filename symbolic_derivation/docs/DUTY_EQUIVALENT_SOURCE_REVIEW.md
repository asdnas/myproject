# Duty-equivalent DSP 源码审查

## 审查范围与约定

- 只读审查：`程序/init.c`、`程序/llc.cla`、`程序/main.c`。
- 用户已确认：`d1=D1`、`d2=D2`、`fai=phi`。
- 当前忽略 dead-band 延时，但保留 `POLSEL` 决定的 A/B 极性。
- physical 电压定义保持 `vL=v1_state*V1-v2_state*n*V2`。

## CMPA 与相移公式

令 `P=TBPRDVAL=428`。忽略限幅、量化和整数截断：

| 寄存器 | 理想公式 | 代码位置 |
|---|---|---|
| CMPA1 | `(D1/2)P` | `llc.cla:982-1001,1021` |
| CMPA2 | `(1-D1/2)P` | `llc.cla:1022` |
| CMPA3 | `(D2/2)P` | `llc.cla:983,1002-1006,1023` |
| CMPA4 | `(1-D2/2)P` | `llc.cla:1024` |
| TBPHS3/4 | `Abs(phi)*(2/3)P` | `llc.cla:1008-1027` |

`main.c:465` 明确记录 `Delta_t/Tsw=fai/3`。因此副边相移时间幅值为：

`Abs(phi)*Ts/3 = (2*Abs(phi)/3)*Th`

这与当前 traditional TPS 分段使用的 `phi*Th` 不同。

## 接线表与理想 A/B 极性

用户确认接线：

| ePWM | switch | ePWM | switch |
|---|---|---|---|
| EPWM1A | S1 | EPWM1B | S2 |
| EPWM2A | S3 | EPWM2B | S4 |
| EPWM3A | Q1 | EPWM3B | Q2 |
| EPWM4A | Q3 | EPWM4B | Q4 |

全部模块使用 up-down 计数和 `CAU=clear/CAD=set`。忽略延时时：

- `POLSEL=2`：A=`RAW_A`，B=`!RAW_A`，用于 EPWM1/3；
- `POLSEL=1`：A=`!RAW_A`，B=`RAW_A`，用于 EPWM2/4。

因此：

- `S1=raw1, S2=!raw1, S3=!raw2, S4=raw2`；
- `Q1=raw3, Q2=!raw3, Q3=!raw4, Q4=raw4`。

由桥规则可恢复原副边三电平电压。

## RAW 边沿

对 `CMPA=cP`：

- RAW_A 在 `c*Ts/2` 发生 CAU 清零；
- RAW_A 在 `Ts-c*Ts/2` 发生 CAD 置位；
- RAW_A 高电平跨越周期边界。

完整 S1...Q4 理想导通端点由 `duty_equivalent_edges.py` 输出。

## 相移 case

- `case_source_actual`：当前源码，`phase_time=phi*Ts/3`。
- `case_corrected_expected`：理论修正，`phase_time=phi*Ts/2=phi*Th`。

用户已确认 `fai=phi_paper`，因此 corrected case 是理论正确关系。两种 case 均按正常功率方向处理：正 phi 时原边超前、副边滞后。

## 关键发现

桥电压脉宽与 TPS 相同，但副边桥整体相移为 `(2phi/3)Th`，不是 `phi*Th`：

- source actual：G 仍保持固定 8 段；D 出现负候选段。
- corrected expected：D/G 都与 traditional TPS 逐段完全一致。

## TODO

1. 修改源码后用实测波形确认 PHSDIR 正方向和相移幅值。
2. 后续若考虑实际门极应力，再加入 DBRED/DBFED；当前结果为忽略死区的理想边界。
