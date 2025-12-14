"""
Системы координат и преобразования между ними
"""
import math
from typing import List, Tuple, Dict, Any


class CoordinateSystem:
    """Управление системами координат и преобразованиями"""
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        
        # Параметры текущей системы координат
        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.rotation = 0.0  # в радианах
    
    def set_center(self, x: float, y: float):
        """Установка центральной точки"""
        self.center_x = x
        self.center_y = y
    
    def set_scale(self, scale: float):
        """Установка масштаба"""
        self.scale = scale
    
    def set_offset(self, dx: float, dy: float):
        """Установка смещения"""
        self.offset_x = dx
        self.offset_y = dy
    
    def set_rotation(self, angle_radians: float):
        """Установка угла поворота"""
        self.rotation = angle_radians
    
    def local_to_screen(self, local_x: float, local_y: float) -> Tuple[float, float]:
        """
        Преобразование локальных координат в экранные
        
        Args:
            local_x, local_y: Координаты в локальной системе
            
        Returns:
            Экранные координаты (x, y)
        """
        # Применяем масштаб
        x = local_x * self.scale
        y = local_y * self.scale
        
        # Применяем поворот
        if self.rotation != 0:
            cos_a = math.cos(self.rotation)
            sin_a = math.sin(self.rotation)
            x_rot = x * cos_a - y * sin_a
            y_rot = x * sin_a + y * cos_a
            x, y = x_rot, y_rot
        
        # Применяем смещение
        x += self.offset_x
        y += self.offset_y
        
        # Центрируем
        x += self.center_x
        y += self.center_y
        
        return x, y
    
    def screen_to_local(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """
        Преобразование экранных координат в локальные
        
        Args:
            screen_x, screen_y: Координаты на экране
            
        Returns:
            Локальные координаты (x, y)
        """
        # Убираем центрирование
        x = screen_x - self.center_x
        y = screen_y - self.center_y
        
        # Убираем смещение
        x -= self.offset_x
        y -= self.offset_y
        
        # Обратный поворот
        if self.rotation != 0:
            cos_a = math.cos(-self.rotation)
            sin_a = math.sin(-self.rotation)
            x_rot = x * cos_a - y * sin_a
            y_rot = x * sin_a + y * cos_a
            x, y = x_rot, y_rot
        
        # Обратный масштаб
        if self.scale != 0:
            x /= self.scale
            y /= self.scale
        
        return x, y
    
    def polar_to_cartesian(self, radius: float, angle: float) -> Tuple[float, float]:
        """
        Преобразование полярных координат в декартовы
        
        Args:
            radius: Расстояние от центра
            angle: Угол в радианах
            
        Returns:
            Декартовы координаты (x, y)
        """
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return x, y
    
    def cartesian_to_polar(self, x: float, y: float) -> Tuple[float, float]:
        """
        Преобразование декартовых координат в полярные
        
        Args:
            x, y: Декартовы координаты
            
        Returns:
            Полярные координаты (radius, angle)
        """
        radius = math.sqrt(x*x + y*y)
        angle = math.atan2(y, x)
        return radius, angle
    
    def apply_pattern_transform(
        self, 
        points: List[float],
        pattern_config: Dict[str, Any]
    ) -> List[Tuple[float, float]]:
        """
        Применение преобразований паттерна к точкам
        
        Args:
            points: Список координат [x1, y1, x2, y2, ...]
            pattern_config: Конфигурация паттерна
            
        Returns:
            Список преобразованных точек [(x1, y1), (x2, y2), ...]
        """
        result = []
        
        # Временное сохранение текущих параметров
        old_scale = self.scale
        old_offset_x = self.offset_x
        old_offset_y = self.offset_y
        old_rotation = self.rotation
        
        # Применяем параметры из конфигурации
        if 'scale' in pattern_config:
            self.scale = pattern_config['scale']
        
        if 'offset' in pattern_config:
            offset = pattern_config['offset']
            self.offset_x = offset[0] if len(offset) > 0 else 0
            self.offset_y = offset[1] if len(offset) > 1 else 0
        
        if 'rotation' in pattern_config:
            self.rotation = pattern_config['rotation']
        
        # Преобразуем точки
        for i in range(0, len(points), 2):
            if i + 1 < len(points):
                local_x = points[i]
                local_y = points[i + 1]
                screen_x, screen_y = self.local_to_screen(local_x, local_y)
                result.append((screen_x, screen_y))
        
        # Восстанавливаем параметры
        self.scale = old_scale
        self.offset_x = old_offset_x
        self.offset_y = old_offset_y
        self.rotation = old_rotation
        
        return result