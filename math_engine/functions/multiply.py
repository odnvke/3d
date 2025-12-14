"""
Умножение функций
"""
import math
from typing import Dict, Any, List
from .base import IFunction


class MultiplyFunction(IFunction):
    """Умножение функций (поэлементное или скалярное)"""
    
    def __init__(self, function_library=None, expression_parser=None):
        self.function_library = function_library
        self.expression_parser = expression_parser
    
    @property
    def function_id(self) -> str:
        return "multiply"
    
    @property
    def required_params(self) -> List[str]:
        return ["functions"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        functions = params.get("functions", [])
        operation = params.get("operation", "elementwise")  # elementwise, scalar_x, scalar_y
        
        if not functions or not self.function_library:
            return [0, 0]
        
        if len(functions) < 2:
            # Если только одна функция, возвращаем её как есть
            func_config = functions[0]
            parsed_config = self._parse_config_with_context(func_config, context)
            func_name = parsed_config.get("func", "circle")
            func = self.function_library.get(func_name)
            return func.evaluate(parsed_config, context)
        
        # Вычисляем первую функцию
        first_config = functions[0]
        parsed_first = self._parse_config_with_context(first_config, context)
        first_func_name = parsed_first.get("func", "circle")
        first_func = self.function_library.get(first_func_name)
        result = first_func.evaluate(parsed_first, context)
        
        # Последовательно умножаем на остальные функции
        for func_config in functions[1:]:
            try:
                parsed_config = self._parse_config_with_context(func_config, context)
                func_name = parsed_config.get("func", "circle")
                func = self.function_library.get(func_name)
                coords = func.evaluate(parsed_config, context)
                
                if len(coords) >= 2 and len(result) >= 2:
                    if operation == "elementwise":
                        result[0] *= coords[0]
                        result[1] *= coords[1]
                    elif operation == "scalar_x":
                        result[0] *= coords[0]
                    elif operation == "scalar_y":
                        result[1] *= coords[1]
                        
            except Exception as e:
                print(f"Error in multiply function: {e}")
        
        return result
    
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