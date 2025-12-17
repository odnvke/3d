"""
Аддон параметрических линий
"""
import pyglet
import time as time_module
from typing import Dict, Any, Optional, List, Callable
from addon_base import BaseAddon
from math_engine.expression_parser import ExpressionParser
from patterns.connect_pattern import ConnectPattern


class ParametricLinesAddon(BaseAddon):
    """Аддон для рисования параметрических линий"""
    
    def __init__(self, window_center_callback: Callable[[], List[int]] = None):
        self.lines = []
        self.batch = None
        self.expression_parser = ExpressionParser()
        self.start_time = time_module.time()
        self.window_center_callback = window_center_callback  # Коллбэк для получения центра
        
        # Регистрация паттернов
        self._register_patterns()
    
    def _register_patterns(self):
        """Регистрация паттернов"""
        self.pattern_classes = {
            'connect': ConnectPattern,
        }
    
    @property
    def addon_id(self) -> str:
        return "parametric_lines"
    
    @property
    def supported_types(self) -> list:
        return ["parametric_lines"]
    
    def validate(self, data: Any) -> bool:
        """Валидация данных"""
        return isinstance(data, dict)
    
    def create_batch(self, data: Dict[str, Any], batch: Optional[pyglet.graphics.Batch] = None) -> pyglet.graphics.Batch:
        """Создание линий по паттерну"""
        if batch is None:
            batch = pyglet.graphics.Batch()
        
        self.batch = batch
        self.lines = []
        self.start_time = time_module.time()
        
        # Автоматически получаем центр окна, если не задан явно
        if 'center' not in data and self.window_center_callback:
            center = self.window_center_callback()
            if center:
                data['center'] = center
                print(f"ParametricLines: Using window center {center}")
        
        pattern_name = data.get('pattern', 'connect')
        
        # Создаем паттерн
        pattern = ConnectPattern()
        
        # Настраиваем паттерн
        pattern.set_config(data)
        pattern.set_expression_parser(self.expression_parser)
        
        # Создаем линии
        self._create_pattern_lines(pattern, data)
        
        return batch
    
    def _create_pattern_lines(self, pattern, config: Dict[str, Any]):
        """Создание графических линий для паттерна"""
        line_count = pattern.get_line_count()
        
        if line_count == 0:
            return
        
        current_time = time_module.time() - self.start_time
        
        for n in range(line_count):
            try:
                # Получаем координаты линии
                (start_x, start_y), (end_x, end_y) = pattern.calculate_line(n, current_time)
                
                # Белый цвет
                color = (255, 255, 255)
                
                # Создаем линию
                line = pyglet.shapes.Line(
                    start_x, start_y,
                    end_x, end_y,
                    color=color,
                    batch=self.batch
                )
                
                self.lines.append({
                    'shape': line,
                    'pattern': pattern,
                    'index': n,
                    'config': config.copy()
                })
                
            except Exception as e:
                print(f"Error creating line {n}: {e}")
                pass
    
    def update_lines(self):
        """Обновление линий на основе текущего времени"""
        if not self.batch or not self.lines:
            return
        
        current_time = time_module.time() - self.start_time
        
        for line_info in self.lines:
            try:
                pattern = line_info['pattern']
                n = line_info['index']
                line = line_info['shape']
                
                # Вычисляем новые координаты
                (start_x, start_y), (end_x, end_y) = pattern.calculate_line(n, current_time)
                
                # Обновляем линию
                line.x = start_x
                line.y = start_y
                line.x2 = end_x
                line.y2 = end_y
                
            except Exception as e:
                print(f"Error updating line: {e}")
                pass
    
    def draw(self, batch: pyglet.graphics.Batch):
        """Отрисовка с обновлением анимации"""
        self.update_lines()
        batch.draw()