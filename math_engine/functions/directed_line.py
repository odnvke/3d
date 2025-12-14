"""
Функция directed_line - точка на линии между двумя функциями
"""
import math
from typing import Dict, Any, List
from .base import IFunction


class DirectedLineFunction(IFunction):
    """Точка на линии между двумя функциями с расстоянием от начала"""
    
    def __init__(self, function_library=None, expression_parser=None):
        self.function_library = function_library
        self.expression_parser = expression_parser
    
    @property
    def function_id(self) -> str:
        return "directed_line"
    
    @property
    def required_params(self) -> List[str]:
        return ["from", "to", "distance"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        # Получаем параметры
        from_config = params.get("from", {})
        to_config = params.get("to", {})
        distance_expr = params.get("distance", "0")
        offset_expr = params.get("offset", "0")
        rotation_expr = params.get("rotation", "0")
        
        if not self.function_library or not self.expression_parser:
            return [0, 0]
        
        try:
            # Вычисляем начальную и конечную точки
            from_func_name = from_config.get("func", "circle")
            to_func_name = to_config.get("func", "circle")
            
            from_func = self.function_library.get(from_func_name)
            to_func = self.function_library.get(to_func_name)
            
            # Парсим конфигурации с контекстом
            parsed_from = self._parse_config_with_context(from_config, context)
            parsed_to = self._parse_config_with_context(to_config, context)
            
            # Вычисляем точки
            from_point = from_func.evaluate(parsed_from, context)
            to_point = to_func.evaluate(parsed_to, context)
            
            if len(from_point) < 2 or len(to_point) < 2:
                return [0, 0]
            
            # Координаты точек
            x1, y1 = from_point[0], from_point[1]
            x2, y2 = to_point[0], to_point[1]
            
            # Вычисляем текущее расстояние между точками
            dx = x2 - x1
            dy = y2 - y1
            current_length = math.sqrt(dx*dx + dy*dy)
            
            # Если точки совпадают, возвращаем начальную точку
            if current_length < 0.000001:
                return [x1, y1]
            
            # Создаем контекст с current_length для парсинга выражений
            eval_context = {}
            if context:
                eval_context.update(context)
            eval_context.update({
                'current_length': current_length,
                'from_x': x1,
                'from_y': y1,
                'to_x': x2,
                'to_y': y2
            })
            
            # Парсим distance с учетом current_length
            if isinstance(distance_expr, str):
                distance = self.expression_parser.parse(distance_expr, eval_context)
            else:
                distance = float(distance_expr)
            
            # Парсим offset
            if isinstance(offset_expr, str):
                offset = self.expression_parser.parse(offset_expr, eval_context)
            else:
                offset = float(offset_expr)
            
            # Парсим rotation
            if isinstance(rotation_expr, str):
                rotation = self.expression_parser.parse(rotation_expr, eval_context)
            else:
                rotation = float(rotation_expr)
            
            # Нормализованный вектор направления
            dir_x = dx / current_length
            dir_y = dy / current_length
            
            # Применяем поворот к направлению
            if rotation != 0:
                cos_r = math.cos(rotation)
                sin_r = math.sin(rotation)
                dir_x_rot = dir_x * cos_r - dir_y * sin_r
                dir_y_rot = dir_x * sin_r + dir_y * cos_r
                dir_x, dir_y = dir_x_rot, dir_y_rot
            
            # Вычисляем точку на линии
            point_x = x1 + dir_x * distance
            point_y = y1 + dir_y * distance
            
            # Применяем перпендикулярное смещение
            if offset != 0:
                # Перпендикулярный вектор (поворот на 90 градусов)
                perp_x = -dir_y
                perp_y = dir_x
                point_x += perp_x * offset
                point_y += perp_y * offset
            
            return [point_x, point_y]
            
        except Exception as e:
            print(f"Error in directed_line function: {e}")
            return [0, 0]
    
    def _parse_config_with_context(self, config: Dict[str, Any], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Парсит конфигурацию функции с использованием expression_parser и контекста"""
        if not self.expression_parser:
            return config
        
        parsed_config = config.copy()
        
        for key, value in config.items():
            if key == "func":
                continue
            
            elif isinstance(value, str):
                # Парсим выражение
                try:
                    parsed_value = self.expression_parser.parse(value, context or {})
                    parsed_config[key] = parsed_value
                except Exception as e:
                    print(f"Error parsing {key}='{value}': {e}")
                    parsed_config[key] = 0.0
        
        return parsed_config