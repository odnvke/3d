"""
Паттерн окружности - линии из центра к точкам на окружности
"""
import math
from typing import Tuple, Dict, Any
from .base_pattern import BasePattern


class CirclePattern(BasePattern):
    """Паттерн окружности (лучи из центра)"""
    
    @property
    def pattern_id(self) -> str:
        return "circle"
    
    def get_line_count(self) -> int:
        """Количество линий = count из конфигурации"""
        return self.config.get('count', 36)
    
    def calculate_line(self, n: int, time: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Вычисление координат для линии n:
        Линия из центра в точку на окружности
        """
        # Получаем параметры
        count = self.get_line_count()
        
        # Центр из конфигурации или по умолчанию 0,0
        center_x = self.config.get('center_x', 0.0)
        center_y = self.config.get('center_y', 0.0)
        
        # Если есть общий center параметр
        if 'center' in self.config:
            center = self.config['center']
            if len(center) >= 2:
                center_x, center_y = center[0], center[1]
        
        # Вычисляем угол с учетом времени
        angle_step = 2 * math.pi / max(1, count)
        angle_offset = self.config.get('angle_offset', 0.0)
        time_factor = self.config.get('time_factor', 0.5)
        
        # Угол для этой линии
        angle = n * angle_step + angle_offset + time * time_factor
        
        # Радиус
        radius = self.config.get('radius', 100.0)
        
        # Конечная точка на окружности
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        
        # Начальная точка - центр
        return ((center_x, center_y), (end_x, end_y))