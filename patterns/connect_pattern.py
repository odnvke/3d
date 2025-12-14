"""Паттерн "connect" - соединение произвольных точек"""
import math
from typing import Tuple, Dict, Any, List
from .base_pattern import BasePattern
from math_engine.function_library import FunctionLibrary


class ConnectPattern(BasePattern):
    """Паттерн соединения точек"""
    
    def __init__(self):
        super().__init__()
        self.function_library = None  # Будет установлен позже
    
    @property
    def pattern_id(self) -> str:
        return "connect"
    
    def get_line_count(self) -> int:
        """Количество линий = (точек - 1) * итераций"""
        points_config = self.config.get('points', [])
        iterations = self.config.get('count', 36)
        return max(0, (len(points_config) - 1) * iterations)
    
    def calculate_line(self, n: int, time: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Вычисление линии n"""
        points_config = self.config.get('points', [])
        if len(points_config) < 2:
            return ((0, 0), (0, 0))
        
        iterations = self.config.get('count', 36)
        points_count = len(points_config)
        
        segment_index = n % (points_count - 1)
        iteration = n // (points_count - 1)
        
        point1 = self._calculate_point_via_library(
            points_config[segment_index], iteration, time
        )
        point2 = self._calculate_point_via_library(
            points_config[segment_index + 1], iteration, time
        )
        
        return (point1, point2)
    
    def _calculate_point_via_library(self, point_config: Dict[str, Any], 
                                    n: int, time: float) -> Tuple[float, float]:
        """Вычисление точки через FunctionLibrary"""
        # Инициализируем function_library если еще не инициализирован
        if self.function_library is None:
            self.function_library = FunctionLibrary(self.expression_parser)
        
        # Получаем имя функции ДО try блока
        func_name = point_config.get('func', 'circle')
        
        try:
            # Копируем конфиг
            params = point_config.copy()
            total_count = self.config.get('count', 36)
            
            context = {
                'n': n,
                'time': time,
                'count': total_count,
                'angle_step': 2 * math.pi / total_count if total_count > 0 else 0,
            }
            
            # Парсим все строковые параметры перед передачей в функцию
            if self.expression_parser:
                parsed_params = {}
                for key, value in params.items():
                    if key == 'func':
                        continue
                    elif isinstance(value, str):
                        # Парсим выражение с контекстом
                        parsed_params[key] = self.expression_parser.parse(value, context)
                    else:
                        parsed_params[key] = value
                params = parsed_params
            
            # Добавляем angle в params если его нет
            if 'angle' not in params:
                # По умолчанию используем n * angle_step
                angle_step = 2 * math.pi / total_count if total_count > 0 else 0
                params['angle'] = n * angle_step
            
            # Вычисляем через библиотеку функций
            coords = self.function_library.evaluate(func_name, params, context)
            
            center_x = self.config.get('center_x', 400)
            center_y = self.config.get('center_y', 300)
            
            if 'center' in self.config:
                center = self.config['center']
                if len(center) >= 2:
                    center_x, center_y = center[0], center[1]
            
            final_x = center_x + coords[0] if len(coords) > 0 else center_x
            final_y = center_y + coords[1] if len(coords) > 1 else center_y
            
            return (final_x, final_y)
                    
        except Exception as e:
            print(f"Error calculating point (func={func_name}): {e}")
            return (400, 300)