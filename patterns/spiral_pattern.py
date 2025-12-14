"""
Паттерн спирали - линии из центра по спирали
"""
import math
from typing import Tuple, Dict, Any
from .base_pattern import BasePattern


class SpiralPattern(BasePattern):
    """Паттерн спирали (Архимедова)"""
    
    @property
    def pattern_id(self) -> str:
        return "spiral"
    
    def get_line_count(self) -> int:
        """Количество линий в спирали"""
        return self.config.get('count', 100)
    
    def calculate_line(self, n: int, time: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Вычисление координат для линии n:
        Линия из центра в точку на спирали
        
        Формула Архимедовой спирали: r = a + b*θ
        """
        count = self.get_line_count()
        center_x = self.config.get('center_x', 0.0)
        center_y = self.config.get('center_y', 0.0)
        
        # Вычисляем угол
        if 'angle_expression' in self.config and self.expression_parser:
            context = {'n': n, 'time': time, 'count': count}
            angle = self.expression_parser.parse(self.config['angle_expression'], context)
        else:
            # По умолчанию: увеличивающийся угол
            max_angle = self.config.get('max_angle', 4 * math.pi)
            time_factor = self.config.get('time_factor', 0.3)
            angle = (n / max(1, count)) * max_angle + time * time_factor
        
        # Вычисляем радиус (растет с углом)
        if 'radius_expression' in self.config and self.expression_parser:
            context = {'n': n, 'time': time, 'count': count, 'angle': angle}
            radius = self.expression_parser.parse(self.config['radius_expression'], context)
        else:
            # Архимедова спираль: r = a + b*θ
            base_radius = self.config.get('base_radius', 10.0)
            growth_factor = self.config.get('growth_factor', 5.0)
            radius = base_radius + growth_factor * angle
        
        # Конечная точка на спирали
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        
        # Начальная точка - центр
        start_x = center_x
        start_y = center_y
        
        return ((start_x, start_y), (end_x, end_y))