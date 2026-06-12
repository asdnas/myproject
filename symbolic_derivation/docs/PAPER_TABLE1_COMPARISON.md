# 论文表1 D/G 开通电流最终核对

仅核对已有论文表1数据的 D/G 四个关键开通事件；未编造其他模式论文表达式。

| mode | event | generated expression | paper expression | diff | status |
|---|---|---|---|---|---|
| D | tS1 | `(-D1*V1 + D1*V2*n - 2*V2*n*phi)/(4*L*fs)` | `(-D1*(V1 - V2*n) - 2*V2*n*phi)/(4*L*fs)` | `0` | **PASS** |
| D | tS4 | `(-D1*V1 - D1*V2*n - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `(-D1*(V1 + V2*n) - 2*V2*n*phi + 2*V2*n)/(4*L*fs)` | `0` | **PASS** |
| D | tQ1 | `(D2*V1 + D2*V2*n + 2*V1*phi - 2*V1)/(4*L*fs)` | `(D2*(V1 + V2*n) + 2*V1*(phi - 1))/(4*L*fs)` | `0` | **PASS** |
| D | tQ4 | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `(-D2*(V1 - V2*n) + 2*V1*phi)/(4*L*fs)` | `0` | **PASS** |
| G | tS1 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `0` | **PASS** |
| G | tS4 | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `(-D1*V1 + D2*V2*n)/(4*L*fs)` | `0` | **PASS** |
| G | tQ1 | `(-D2*V1 + D2*V2*n - 2*V1*phi)/(4*L*fs)` | `(-D2*(V1 - V2*n) - 2*V1*phi)/(4*L*fs)` | `0` | **PASS** |
| G | tQ4 | `(-D2*V1 + D2*V2*n + 2*V1*phi)/(4*L*fs)` | `(-D2*(V1 - V2*n) + 2*V1*phi)/(4*L*fs)` | `0` | **PASS** |
