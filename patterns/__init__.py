"""
Модуль паттернов для генерации линий
"""
from .base_pattern import BasePattern
from .circle_pattern import CirclePattern
from .spiral_pattern import SpiralPattern
from .cube_pattern import CubePattern
#from .grid_pattern import GridPattern
#from .wave_pattern import WavePattern

__all__ = [
    'BasePattern',
    'CirclePattern',
    'SpiralPattern', 
    'CubePattern',
    # 'GridPattern',
    # 'WavePattern'
]