# fai / TBPHS 缩放审查

## 已确认定义

用户已确认：

`fai = phi_paper`

其中 `phi_paper` 是 traditional TPS 原副边桥输出电压中心点相位差，采用半周期 `Th` 归一化。因此理论期望：

`phase_time_expected = fai*Th = fai*Ts/2`

up-down 计数完整周期满足：

`Ts = 2*TBPRD*T_TBCLK`

所以理论比较器相位计数应为：

`phase_count_expected = Abs(fai)*TBPRD`

## 当前源码行为

当前源码使用：

- `main.c:47`：`DAB_PWM_PHASE_SCALE = 2/3`
- `main.c:468,473`：`phase_count = Abs(fai)*(2/3)*TBPRDVAL`
- `llc.cla:252,257,1010,1015`：`phase_count = Abs(fai)*285.333333`

当 `TBPRDVAL=428` 时，`285.333333=(2/3)*428`。因此：

`phase_time_actual = fai*Ts/3 = (2fai/3)*Th`

相对理论期望少：

`phase_time_actual-phase_time_expected = -fai*Ts/6`

## 符号验证

`case_source_actual` 使用当前源码的 `fai*Ts/3`：

- G 的 `tQ1` 电流比 TPS 增加 `V1*fai/(6Lfs)`；
- G 的 `tQ4` 电流比 TPS减少 `V1*fai/(6Lfs)`；
- D 原模式域出现负候选段。

这些差异正好对应少掉的 `fai*Ts/6` 相移。

`case_corrected_expected` 使用理论正确的 `fai*Ts/2`：

- D/G VoltageSegment 与 TPS 逐段完全一致；
- D/G 所有 `I0...I8` 与 TPS 完全一致；
- `tS1/tS4/tQ1/tQ4` 电流差全部为 0；
- 所有 inferred 理想关断边界电流差也全部为 0。

## 结论

在 `fai=phi_paper` 的前提下，当前源码 TBPHS 缩放比例确实错误。理论上应使用：

`TBPHS = Abs(fai)*TBPRD`

本项目未修改 `程序/` 源码，只在符号框架中增加 corrected case。
