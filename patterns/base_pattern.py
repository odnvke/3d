"""
Базовый класс для всех паттернов
"""
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
import math


class BasePattern(ABC):
    """Абстрактный базовый класс паттерна"""
    
    def __init__(self):
        self.config = {}
        self.coord_system = None
        self.expression_parser = None
    
    @property
    @abstractmethod
    def pattern_id(self) -> str:
        """Уникальный идентификатор паттерна"""
        pass
    
    @abstractmethod
    def get_line_count(self) -> int:
        """Количество линий в паттерне"""
        pass
    
    @abstractmethod
    def calculate_line(self, n: int, time: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Вычисление координат для линии n
        """
        pass
    
    def set_config(self, config: Dict[str, Any]):
        """Установка конфигурации паттерна"""
        self.config = config
    
    def set_coordinate_system(self, coord_system):
        """Установка системы координат"""
        self.coord_system = coord_system
    
    def set_expression_parser(self, parser):
        """Установка парсера выражений"""
        self.expression_parser = parser
    
    def get_line_color(self, n: int, time: float) -> Tuple[int, int, int]:
        """
        Получение цвета для линии n
        """
        if 'color' in self.config:
            color = self.config['color']
            if len(color) >= 3:
                return tuple(color[:3])
        
        hue = (n / max(1, self.get_line_count())) * 360
        return self._hsv_to_rgb(hue, 100, 100)
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Преобразование HSV в RGB"""
        h = h % 360
        s = max(0, min(100, s)) / 100
        v = max(0, min(100, v)) / 100
        
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )