"""DAB 符号推导框架。

无法从旧程序或参考论文确认的事件时间和状态机定义会显式保留为 TODO。
"""

from .symbols import D1, D2, L, Th, Ts, V1, V2, fs, n, phi

__all__ = ["D1", "D2", "phi", "V1", "V2", "n", "L", "fs", "Ts", "Th"]
