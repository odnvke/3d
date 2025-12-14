"""
Морфинг между функциями
"""
import math
from typing import Dict, Any, List
from .base import IFunction


class MorphFunction(IFunction):
    """Морфинг (интерполяция) между функциями"""
    
    def __init__(self, function_library=None, expression_parser=None):
        self.function_library = function_library
        self.expression_parser = expression_parser
    
    @property
    def function_id(self) -> str:
        return "morph"
    
    @property
    def required_params(self) -> List[str]:
        return ["functions", "t"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        functions = params.get("functions", [])
        t = params.get("t", 0.0)
        
        if not functions or not self.function_library:
            return [0, 0]
        
        # Если t строка - парсим её
        if isinstance(t, str) and self.expression_parser:
            try:
                t = self.expression_parser.parse(t, context or {})
            except Exception:
                t = 0.0
        t = float(t)
        
        # Ограничиваем t от 0 до 1
        t = max(0.0, min(1.0, t))
        
        if len(functions) == 1:
            # Если только одна функция, возвращаем её
            func_config = functions[0]
            parsed_config = self._parse_config_with_context(func_config, context)
            func_name = parsed_config.get("func", "circle")
            func = self.function_library.get(func_name)
            return func.evaluate(parsed_config, context)
        
        # Вычисляем все функции
        all_coords = []
        for func_config in functions:
            try:
                parsed_config = self._parse_config_with_context(func_config, context)
                func_name = parsed_config.get("func", "circle")
                func = self.function_library.get(func_name)
                coords = func.evaluate(parsed_config, context)
                all_coords.append(coords[:2])  # Берем только x, y
            except Exception as e:
                print(f"Error in morph function: {e}")
                all_coords.append([0.0, 0.0])
        
        if len(all_coords) < 2:
            return [0.0, 0.0]
        
        # Интерполируем между функциями
        segment = t * (len(all_coords) - 1)
        index = int(math.floor(segment))
        fraction = segment - index
        
        if index >= len(all_coords) - 1:
            # Последняя функция
            return all_coords[-1]
        
        # Линейная интерполяция между двумя функциями
        x1, y1 = all_coords[index]
        x2, y2 = all_coords[index + 1]
        
        x = x1 + fraction * (x2 - x1)
        y = y1 + fraction * (y2 - y1)
        
        return [x, y]
    
    def _parse_config_with_context(self, config: Dict[str, Any], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Парсит параметры с использованием expression_parser и контекста"""
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