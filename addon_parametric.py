"""
Аддон параметрических линий - основной аддон для работы с паттернами
"""
import pyglet
import time as time_module
from typing import Dict, Any, Optional, List
from addon_base import BaseAddon
from math_engine.expression_parser import ExpressionParser
from patterns.circle_pattern import CirclePattern
from patterns.spiral_pattern import SpiralPattern
from patterns.cube_pattern import CubePattern


class ParametricLinesAddon(BaseAddon):
    """Аддон для рисования параметрических линий по паттернам"""
    
    def __init__(self):
        self.patterns = {}
        self.lines = []
        self.batch = None
        self.expression_parser = ExpressionParser()
        self.start_time = time_module.time()
        
        # Регистрация доступных паттернов
        self._register_patterns()
    
    def _register_patterns(self):
        """Регистрация всех доступных паттернов"""
        self.pattern_classes = {
            'circle': CirclePattern,
            'spiral': SpiralPattern,
            'cube': CubePattern,
        }
    
    @property
    def addon_id(self) -> str:
        return "parametric_lines"
    
    @property
    def supported_types(self) -> list:
        return ["parametric_lines"]
    
    def validate(self, data: Any) -> bool:
        """Валидация данных параметрических линий"""
        return isinstance(data, dict)
    
    def create_batch(self, data: Dict[str, Any], batch: Optional[pyglet.graphics.Batch] = None) -> pyglet.graphics.Batch:
        """Создание линий по паттерну"""
        if batch is None:
            batch = pyglet.graphics.Batch()
        
        self.batch = batch
        self.lines = []
        self.start_time = time_module.time()
        
        print(f"ParametricLinesAddon: Creating pattern '{data.get('pattern', 'unknown')}'")
        
        # Создаем паттерн
        pattern_name = data.get('pattern', 'circle')
        pattern_class = self.pattern_classes.get(pattern_name, CirclePattern)
        pattern = pattern_class()
        
        # Настраиваем паттерн
        pattern.set_config(data)
        pattern.set_expression_parser(self.expression_parser)
        
        # Создаем линии
        self._create_pattern_lines(pattern, data)
        
        return batch
    
    def _create_pattern_lines(self, pattern, config: Dict[str, Any]):
        """Создание графических линий для паттерна"""
        line_count = pattern.get_line_count()
        print(f"  Creating {line_count} lines for pattern '{pattern.pattern_id}'")
        
        current_time = time_module.time() - self.start_time
        
        for n in range(line_count):
            try:
                # Получаем координаты линии
                (start_x, start_y), (end_x, end_y) = pattern.calculate_line(n, current_time)
                
                # СДВИГАЕМ В ЦЕНТР ЭКРАНА!
                # Если center не указан, используем центр экрана
                if 'center' not in config:
                    start_x += 512  # половина ширины 1024
                    start_y += 384  # половина высоты 768
                    end_x += 512
                    end_y += 384
                
                # Получаем цвет
                color = pattern.get_line_color(n, current_time)
                
                # Создаем линию Pyglet
                line = pyglet.shapes.Line(
                    start_x, start_y,
                    end_x, end_y,
                    color=color,
                    batch=self.batch
                )
                
                # Устанавливаем толщину
                line.width = config.get('line_width', 2)
                
                self.lines.append({
                    'shape': line,
                    'pattern': pattern,
                    'index': n,
                    'config': config
                })
                
            except Exception as e:
                print(f"  Error creating line {n}: {e}")
    
    def update_lines(self):
        """Обновление линий на основе текущего времени"""
        if not self.batch:
            return
        
        current_time = time_module.time() - self.start_time
        
        for line_info in self.lines:
            try:
                pattern = line_info['pattern']
                n = line_info['index']
                line = line_info['shape']
                config = line_info['config']
                
                # Вычисляем новые координаты
                (start_x, start_y), (end_x, end_y) = pattern.calculate_line(n, current_time)
                
                # СДВИГАЕМ В ЦЕНТР ЭКРАНА!
                if 'center' not in config:
                    start_x += 512
                    start_y += 384
                    end_x += 512
                    end_y += 384
                
                # Обновляем линию
                line.x = start_x
                line.y = start_y
                line.x2 = end_x
                line.y2 = end_y
                
                # Обновляем цвет
                color = pattern.get_line_color(n, current_time)
                line.color = color
                
            except Exception as e:
                print(f"Error updating line: {e}")
    
    def draw(self, batch: pyglet.graphics.Batch):
        """Отрисовка с обновлением анимации"""
        # Обновляем линии
        self.update_lines()
        
        # Рисуем
        batch.draw()