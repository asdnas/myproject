# Traditional TPS 最终符号公式检查

- A-H 均有 I0...I8：PASS
- A-H 均有 tS1/tS4/tQ1/tQ4：PASS
- A-H 均有 8 个 inferred 关断事件：PASS
- 所有输出电流来自 mode_currents_symbolic.csv：PASS
- 未凭空生成新电流：PASS
- D/G 论文表1核对：PASS

## 论文使用建议

- `AH_TURN_ON_CURRENT_TABLE_FOR_PAPER.md` 中 confirmed 开通公式可直接用于论文。
- `AH_TURN_OFF_CURRENT_TABLE_FOR_PAPER.md` 必须标注为 inferred、ideal boundary current、dead time ignored。
- 建议人工复核图3未直接标注的关断事件命名，以及实际含死区时的关断电流取值时刻。
- A/C/E/F/H 没有论文表1对照数据，未进行外部公式核对。
