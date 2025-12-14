"""
Сумма нескольких функций
"""
from typing import Dict, Any, List
from .base import IFunction


class SumFunction(IFunction):
    """Сумма нескольких функций"""
    
    def __init__(self, function_library=None, expression_parser=None):
        self.function_library = function_library
        self.expression_parser = expression_parser
    
    @property
    def function_id(self) -> str:
        return "sum"
    
    @property
    def required_params(self) -> List[str]:
        return ["functions"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        functions = params.get("functions", [])
        
        if not functions or not self.function_library:
            return [0, 0]
        
        total_x, total_y = 0.0, 0.0
        
        for func_config in functions:
            try:
                # Парсим параметры с контекстом
                parsed_config = self._parse_config_with_context(func_config, context)
                
                func_name = parsed_config.get("func", "circle")
                func = self.function_library.get(func_name)
                
                # Вычисляем координаты
                coords = func.evaluate(parsed_config, context)
                
                if len(coords) >= 2:
                    total_x += coords[0]
                    total_y += coords[1]
                    
            except Exception as e:
                print(f"Error in sum function: {e}")
        
        return [total_x, total_y]
    
    def _parse_config_with_context(self, config: Dict[str, Any], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Парсит параметры с использованием expression_parser и контекста"""
        if not self.expression_parser:
            return config
        
        parsed_config = config.copy()
        
        for key, value in config.items():
            if key == "func":
                continue
            
            elif key == "functions":
                # Рекурсивно парсим вложенные функции
                if isinstance(value, list):
                    parsed_functions = []
                    for func_item in value:
                        if isinstance(func_item, dict):
                            parsed_functions.append(
                                self._parse_config_with_context(func_item, context)
                            )
                        else:
                            parsed_functions.append(func_item)
                    parsed_config[key] = parsed_functions
            
            elif isinstance(value, str):
                # Парсим выражение
                try:
                    parsed_value = self.expression_parser.parse(value, context or {})
                    parsed_config[key] = parsed_value
                except Exception as e:
                    print(f"Error parsing {key}='{value}': {e}")
                    parsed_config[key] = 0.0
        
        return parsed_config