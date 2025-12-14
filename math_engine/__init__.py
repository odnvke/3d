"""
Математический движок для параметрических линий
Обеспечивает вычисление выражений, функций и преобразование координат
"""

from .expression_parser import ExpressionParser
from .function_library import FunctionLibrary
from .coordinate_system import CoordinateSystem
from .animation_engine import AnimationEngine

__all__ = [
    'ExpressionParser',
    'FunctionLibrary', 
    'CoordinateSystem',
    'AnimationEngine'
]