"""
Модуль паттернов - ТОЛЬКО connect
"""
from .base_pattern import BasePattern
from .connect_pattern import ConnectPattern

__all__ = [
    'BasePattern',
    'ConnectPattern'  # ← только один паттерн
]