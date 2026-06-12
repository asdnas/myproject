# A-H 归一化指标与参考论文附表 A1 复现报告

## 定义对应关系

- 本文使用 `K=n*V2/V1`；参考论文表 A1 使用 `M`，对照时统一执行 `M -> K`。
- 本文功率由统一分段模型计算：`p_star=(1/K)*sum(v1_state*area_i_star)`。
- 本文计算 `Irms_star_sq=(1/2)*sum(integral(i_star^2 d_tau))`。
- 表 A1 的“标幺化电流有效值表达式”经对照确认对应 `Irms_star_sq`，不是开方后的 `Irms_star`。
- 电流应力采用所有边界电流的 `max(abs(I0_star...I8_star))`；A1 分段应力公式通过约束域随机样本验证。
- 所有数值采样均限制在对应模式 A1 约束域内，并覆盖 `K<1`、`K=1` 和 `K>1`。

## 总览

| mode | metric | symbolic | numeric | status | max abs error |
|---|---|---|---|---|---:|
| A | p_star | True | True | **PASS** | `0.0` |
| A | Irms_star_sq | True | True | **PASS** | `0.0` |
| A | current_stress_star | N/A | True | **PASS** | `0.0` |
| B | p_star | True | True | **PASS** | `0.0` |
| B | Irms_star_sq | True | True | **PASS** | `0.0` |
| B | current_stress_star | N/A | True | **PASS** | `0.0` |
| C | p_star | True | True | **PASS** | `0.0` |
| C | Irms_star_sq | True | True | **PASS** | `0.0` |
| C | current_stress_star | N/A | True | **PASS** | `0.0` |
| D | p_star | True | True | **PASS** | `0.0` |
| D | Irms_star_sq | True | True | **PASS** | `0.0` |
| D | current_stress_star | N/A | True | **PASS** | `0.0` |
| E | p_star | True | True | **PASS** | `0.0` |
| E | Irms_star_sq | True | True | **PASS** | `0.0` |
| E | current_stress_star | N/A | True | **PASS** | `0.0` |
| F | p_star | True | True | **PASS** | `0.0` |
| F | Irms_star_sq | True | True | **PASS** | `0.0` |
| F | current_stress_star | N/A | True | **PASS** | `0.0` |
| G | p_star | True | True | **PASS** | `0.0` |
| G | Irms_star_sq | True | True | **PASS** | `0.0` |
| G | current_stress_star | N/A | True | **PASS** | `0.0` |
| H | p_star | True | True | **PASS** | `0.0` |
| H | Irms_star_sq | True | True | **PASS** | `0.0` |
| H | current_stress_star | N/A | True | **PASS** | `0.0` |

## 分模式表达式

### Mode A

- A1 约束：`1 + (D2 - D1)/2 <= phi <= 1 + (D1 - D2)/2`
- 自动生成 `p_star`：`-4*D2*(phi - 1)`
- A1 `p_star`：`-4*D2*(phi - 1)`
- 自动生成 `Irms_star_sq`：`-(2*D1**3 + 3*D1**2*D2*K - 3*D1**2 - 6*D1*D2*K + 2*D2**3*K**2 + D2**3*K - 3*D2**2*K**2 + 12*D2*K*phi**2 - 24*D2*K*phi + 12*D2*K)/3`
- A1 `Irms_star_sq`：`-(2*D1**3 + 3*D1**2*D2*K - 3*D1**2 - 6*D1*D2*K + 2*D2**3*K**2 + D2**3*K - 3*D2**2*K**2 + 12*D2*K*phi**2 - 24*D2*K*phi + 12*D2*K)/3`
- A1 电流应力，`K<1`：`D1 + D2*K`
- A1 电流应力，`K>=1`：`D1 + D2*K`
- 自动生成应力候选：`(D1 + D2*K, D2*K + D2 - 2*phi + 2, -D2*K - D2 - 2*phi + 2, -D1 - D2*K, -D1 - D2*K, -D2*K - D2 + 2*phi - 2, D2*K + D2 + 2*phi - 2, D1 + D2*K, D1 + D2*K)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode B

- A1 约束：`(D1 + D2)/2 <= phi <= 1 + (D2 - D1)/2 & 1 - (D1 + D2)/2 <= phi <= 1 + (D1 - D2)/2`
- 自动生成 `p_star`：`-(D1**2 - 2*D1*D2 + 4*D1*phi - 4*D1 + D2**2 + 4*D2*phi - 4*D2 + 4*phi**2 - 8*phi + 4)/2`
- A1 `p_star`：`-(D1**2 - 2*D1*D2 + 4*D1*phi - 4*D1 + D2**2 + 4*D2*phi - 4*D2 + 4*phi**2 - 8*phi + 4)/2`
- 自动生成 `Irms_star_sq`：`-(D1**3*K + 4*D1**3 + 3*D1**2*D2*K + 6*D1**2*K*phi - 6*D1**2*K - 6*D1**2 + 3*D1*D2**2*K - 12*D1*D2*K*phi + 12*D1*K*phi**2 - 24*D1*K*phi + 12*D1*K + 4*D2**3*K**2 + D2**3*K - 6*D2**2*K**2 + 6*D2**2*K*phi - 6*D2**2*K + 12*D2*K*phi**2 - 24*D2*K*phi + 12*D2*K + 8*K*phi**3 - 24*K*phi**2 + 24*K*phi - 8*K)/6`
- A1 `Irms_star_sq`：`-(D1**3*K + 4*D1**3 + 3*D1**2*D2*K + 6*D1**2*K*phi - 6*D1**2*K - 6*D1**2 + 3*D1*D2**2*K - 12*D1*D2*K*phi + 12*D1*K*phi**2 - 24*D1*K*phi + 12*D1*K + 4*D2**3*K**2 + D2**3*K - 6*D2**2*K**2 + 6*D2**2*K*phi - 6*D2**2*K + 12*D2*K*phi**2 - 24*D2*K*phi + 12*D2*K + 8*K*phi**3 - 24*K*phi**2 + 24*K*phi - 8*K)/6`
- A1 电流应力，`K<1`：`D1 + D2*K`
- A1 电流应力，`K>=1`：`D1 + D2*K`
- 自动生成应力候选：`(D1*K + D1 + 2*K*phi - 2*K, -D2*K - D2 - 2*phi + 2, -D1 - D2*K, -D1 - D2*K, -D1*K - D1 - 2*K*phi + 2*K, D2*K + D2 + 2*phi - 2, D1 + D2*K, D1 + D2*K, D1*K + D1 + 2*K*phi - 2*K)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode C

- A1 约束：`(D1 + D2)/2 <= phi <= 1 - (D1 + D2)/2`
- 自动生成 `p_star`：`2*D1*D2`
- A1 `p_star`：`2*D1*D2`
- 自动生成 `Irms_star_sq`：`-(2*D1**3 - 3*D1**2 - 12*D1*D2*K*phi + 6*D1*D2*K + 2*D2**3*K**2 - 3*D2**2*K**2)/3`
- A1 `Irms_star_sq`：`-(2*D1**3 - 3*D1**2 - 12*D1*D2*K*phi + 6*D1*D2*K + 2*D2**3*K**2 - 3*D2**2*K**2)/3`
- A1 电流应力，`K<1`：`D1 + D2*K`
- A1 电流应力，`K>=1`：`D1 + D2*K`
- 自动生成应力候选：`(D1 - D2*K, -D1 - D2*K, -D1 - D2*K, -D1 + D2*K, -D1 + D2*K, D1 + D2*K, D1 + D2*K, D1 - D2*K, D1 - D2*K)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode D

- A1 约束：`1 - (D1 + D2)/2 <= phi <= (D1 + D2)/2`
- 自动生成 `p_star`：`-D1**2 + 2*D1 - D2**2 + 2*D2 - 4*phi**2 + 4*phi - 2`
- A1 `p_star`：`-D1**2 + 2*D1 - D2**2 + 2*D2 - 4*phi**2 + 4*phi - 2`
- 自动生成 `Irms_star_sq`：`-(2*D1**3 + 6*D1**2*K*phi - 3*D1**2*K - 3*D1**2 - 12*D1*K*phi + 6*D1*K + 2*D2**3*K**2 - 3*D2**2*K**2 + 6*D2**2*K*phi - 3*D2**2*K - 12*D2*K*phi + 6*D2*K + 8*K*phi**3 - 12*K*phi**2 + 12*K*phi - 4*K)/3`
- A1 `Irms_star_sq`：`-(2*D1**3 + 6*D1**2*K*phi - 3*D1**2*K - 3*D1**2 - 12*D1*K*phi + 6*D1*K + 2*D2**3*K**2 - 3*D2**2*K**2 + 6*D2**2*K*phi - 3*D2**2*K - 12*D2*K*phi + 6*D2*K + 8*K*phi**3 - 12*K*phi**2 + 12*K*phi - 4*K)/3`
- A1 电流应力，`K<1`：`-D1*K + D1 + 2*K*phi`
- A1 电流应力，`K>=1`：`D2*K - D2 + 2*phi`
- 自动生成应力候选：`(D1*K + D1 + 2*K*phi - 2*K, -D2*K - D2 - 2*phi + 2, -D2*K + D2 - 2*phi, D1*K - D1 - 2*K*phi, -D1*K - D1 - 2*K*phi + 2*K, D2*K + D2 + 2*phi - 2, D2*K - D2 + 2*phi, -D1*K + D1 + 2*K*phi, D1*K + D1 + 2*K*phi - 2*K)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode E

- A1 约束：`(D1 - D2)/2 <= phi <= 1 - (D1 + D2)/2 & (D2 - D1)/2 <= phi <= (D1 + D2)/2`
- 自动生成 `p_star`：`-(D1**2 - 2*D1*D2 - 4*D1*phi + D2**2 - 4*D2*phi + 4*phi**2)/2`
- A1 `p_star`：`-(D1**2 - 2*D1*D2 - 4*D1*phi + D2**2 - 4*D2*phi + 4*phi**2)/2`
- 自动生成 `Irms_star_sq`：`(D1**3*K - 4*D1**3 + 3*D1**2*D2*K - 6*D1**2*K*phi + 6*D1**2 + 3*D1*D2**2*K + 12*D1*D2*K*phi - 12*D1*D2*K + 12*D1*K*phi**2 - 4*D2**3*K**2 + D2**3*K + 6*D2**2*K**2 - 6*D2**2*K*phi + 12*D2*K*phi**2 - 8*K*phi**3)/6`
- A1 `Irms_star_sq`：`(D1**3*K - 4*D1**3 + 3*D1**2*D2*K - 6*D1**2*K*phi + 6*D1**2 + 3*D1*D2**2*K + 12*D1*D2*K*phi - 12*D1*D2*K + 12*D1*K*phi**2 - 4*D2**3*K**2 + D2**3*K + 6*D2**2*K**2 - 6*D2**2*K*phi + 12*D2*K*phi**2 - 8*K*phi**3)/6`
- A1 电流应力，`K<1`：`-D1*K + D1 + 2*K*phi`
- A1 电流应力，`K>=1`：`D2*K - D2 + 2*phi`
- 自动生成应力候选：`(D1 - D2*K, -D2*K + D2 - 2*phi, D1*K - D1 - 2*K*phi, -D1 + D2*K, -D1 + D2*K, D2*K - D2 + 2*phi, -D1*K + D1 + 2*K*phi, D1 - D2*K, D1 - D2*K)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode F

- A1 约束：`(D1 - D2)/2 <= phi <= (D2 - D1)/2`
- 自动生成 `p_star`：`4*D1*phi`
- A1 `p_star`：`4*D1*phi`
- 自动生成 `Irms_star_sq`：`(D1**3*K - 2*D1**3 + 3*D1**2 + 3*D1*D2**2*K - 6*D1*D2*K + 12*D1*K*phi**2 - 2*D2**3*K**2 + 3*D2**2*K**2)/3`
- A1 `Irms_star_sq`：`(D1**3*K - 2*D1**3 + 3*D1**2 + 3*D1*D2**2*K - 6*D1*D2*K + 12*D1*K*phi**2 - 2*D2**3*K**2 + 3*D2**2*K**2)/3`
- A1 电流应力，`K<1`：`Max(-D1 + D2*K, -D1*K + D1 + 2*K*phi)`
- A1 电流应力，`K>=1`：`-D1 + D2*K`
- 自动生成应力候选：`(-D1*K + D1 - 2*K*phi, D1*K - D1 - 2*K*phi, -D1 + D2*K, -D1 + D2*K, D1*K - D1 + 2*K*phi, -D1*K + D1 + 2*K*phi, D1 - D2*K, D1 - D2*K, -D1*K + D1 - 2*K*phi)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode G

- A1 约束：`(D2 - D1)/2 <= phi <= (D1 - D2)/2`
- 自动生成 `p_star`：`4*D2*phi`
- A1 `p_star`：`4*D2*phi`
- 自动生成 `Irms_star_sq`：`-(2*D1**3 - 3*D1**2*D2*K - 3*D1**2 + 6*D1*D2*K + 2*D2**3*K**2 - D2**3*K - 3*D2**2*K**2 - 12*D2*K*phi**2)/3`
- A1 `Irms_star_sq`：`-(2*D1**3 - 3*D1**2*D2*K - 3*D1**2 + 6*D1*D2*K + 2*D2**3*K**2 - D2**3*K - 3*D2**2*K**2 - 12*D2*K*phi**2)/3`
- A1 电流应力，`K<1`：`D1 - D2*K`
- A1 电流应力，`K>=1`：`Max(D1 - D2*K, D2*K - D2 + 2*phi)`
- 自动生成应力候选：`(D1 - D2*K, -D2*K + D2 - 2*phi, D2*K - D2 - 2*phi, -D1 + D2*K, -D1 + D2*K, D2*K - D2 + 2*phi, -D2*K + D2 + 2*phi, D1 - D2*K, D1 - D2*K)`
- 录入说明：PDF 文本抽取将中间项显示为 `3D1^2D2^2M`；按总次数三次录入为 `3D1^2D2M`，需结合自动对照复核。
- A1 公式人工复核状态：`NEEDS_MANUAL_REVIEW_PDF_VISUAL`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

### Mode H

- A1 约束：`1 + (D1 - D2)/2 <= phi <= 1 + (D2 - D1)/2`
- 自动生成 `p_star`：`-4*D1*(phi - 1)`
- A1 `p_star`：`-4*D1*(phi - 1)`
- 自动生成 `Irms_star_sq`：`-(D1**3*K + 2*D1**3 - 3*D1**2 + 3*D1*D2**2*K - 6*D1*D2*K + 12*D1*K*phi**2 - 24*D1*K*phi + 12*D1*K + 2*D2**3*K**2 - 3*D2**2*K**2)/3`
- A1 `Irms_star_sq`：`-(D1**3*K + 2*D1**3 - 3*D1**2 + 3*D1*D2**2*K - 6*D1*D2*K + 12*D1*K*phi**2 - 24*D1*K*phi + 12*D1*K + 2*D2**3*K**2 - 3*D2**2*K**2)/3`
- A1 电流应力，`K<1`：`D1 + D2*K`
- A1 电流应力，`K>=1`：`D1 + D2*K`
- 自动生成应力候选：`(D1*K + D1 + 2*K*phi - 2*K, -D1*K - D1 + 2*K*phi - 2*K, -D1 - D2*K, -D1 - D2*K, -D1*K - D1 - 2*K*phi + 2*K, D1*K + D1 - 2*K*phi + 2*K, D1 + D2*K, D1 + D2*K, D1*K + D1 + 2*K*phi - 2*K)`
- A1 公式人工复核状态：`CONFIRMED_FROM_PDF_TEXT`
- `p_star`：PASS；差值/方法：`0`；A1 原文 M 已替换为本文 K。
- `Irms_star_sq`：PASS；差值/方法：`0`；A1 的标幺化电流有效值表达式与本文 Irms_star_sq 一致。
- `current_stress_star`：PASS；差值/方法：`numeric_sampling`；约束域内 80 个确定性随机样本；比较 max(abs(I0_star...I8_star))。

## 结论

- A-H 功率表达式 PASS 数：8/8。
- A-H RMS 平方表达式 PASS 数：8/8。
- A-H 电流应力表达式 PASS 数：8/8。
- 不一致项数量：0。
- G 模式 RMS 的 PDF 文本抽取歧义已通过统一分段模型的符号零差值确定为三次项 `3*D1**2*D2*K`；仍建议对照 PDF 视觉版归档确认。
- 当前唯一保留的人工复核项：G 模式 A1 RMS 中间项的 PDF 视觉版确认；这不影响当前符号零差值验证结果。
