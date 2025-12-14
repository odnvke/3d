"""
Паттерн "connect" - соединение произвольных точек
"""
import math
from typing import Tuple, Dict, Any, List
from .base_pattern import BasePattern
from math_engine.function_library import FunctionLibrary


class ConnectPattern(BasePattern):
    """
    Паттерн соединения точек
    n остаётся как есть (не умножается на angle_step)
    """
    
    def __init__(self):
        super().__init__()
        self.function_library = FunctionLibrary()
    
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
        
        # Определяем какие точки соединяем
        segment_index = n % (points_count - 1)
        iteration = n // (points_count - 1)
        
        # Вычисляем точки
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
        func_name = point_config.get('func', 'circle')
        
        try:
            params = point_config.copy()
            total_count = self.config.get('count', 36)
            
            # Контекст для парсера
            context = {
                'n': n,
                'time': time,
                'count': total_count,
                'angle_step': 2 * math.pi / total_count,
            }
            
            # Если есть angle - парсим только если это строка
            if 'angle' in params:
                angle_value = params['angle']
                
                if isinstance(angle_value, str):
                    # Это выражение - парсим
                    parsed_angle = self.expression_parser.parse(angle_value, context)
                    params['angle'] = parsed_angle
                else:
                    # Уже число - оставляем как есть
                    params['angle'] = float(angle_value)
            
            # Вычисляем координаты
            coords = self.function_library.evaluate(func_name, params)
            
            # Применяем смещение центра
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
            print(f"Error calculating point: {e}")
            import traceback
            traceback.print_exc()
            return (400, 300)