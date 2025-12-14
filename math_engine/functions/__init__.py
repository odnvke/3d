"""
Функции для математического движка
"""
from .base import IFunction
from .circle import CircleFunction
from .square import SquareFunction
from .fixed import FixedFunction
from .ngon import NGonFunction
from .sum import SumFunction
from .multiply import MultiplyFunction
from .morph import MorphFunction
from .directed_line import DirectedLineFunction  # <-- Добавляем

__all__ = [
    'IFunction',
    'CircleFunction',
    'SquareFunction',
    'FixedFunction',
    'NGonFunction',
    'SumFunction',
    'MultiplyFunction',
    'MorphFunction',
    'DirectedLineFunction'  # <-- Добавляем
]