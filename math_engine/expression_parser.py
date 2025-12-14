"""
Парсер математических выражений с поддержкой time, n и пользовательских функций
"""
import math
import re
from typing import Any, Dict, Callable, Union


class ExpressionParser:
    """Безопасный парсер математических выражений"""
    
    def __init__(self, function_library=None):
        self.function_library = function_library
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Настройка встроенных математических функций и констант"""
        self.builtins = {
            # Константы
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            
            # Тригонометрические функции
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            
            # Другие функции
            'abs': abs,
            'round': round,
            'sqrt': math.sqrt,
            'log': math.log,
            'exp': math.exp,
            'floor': math.floor,
            'ceil': math.ceil,
        }
    
    def parse(self, expression: str, context: Dict[str, Any] = None) -> float:
        """
        Парсит и вычисляет математическое выражение
        """
        if context is None:
            context = {}
        
        try:
            # Очищаем выражение
            expr = expression.strip()
            if not expr:
                return 0.0
            
            # Создаем контекст для eval
            eval_context = {**self.builtins, **context}
            
            # Безопасное вычисление
            result = self._evaluate_safely(expr, eval_context)
            return float(result)
            
        except Exception as e:
            print(f"Error parsing expression '{expression}': {e}")
            return 0.0
    
    def _evaluate_safely(self, expr: str, context: Dict[str, Any]) -> float:
        """Безопасное вычисление выражения"""
        # Разрешенные функции и переменные
        allowed_names = set(context.keys())
        
        # Компилируем с ограничениями
        code = compile(expr, "<string>", "eval")
        
        # Проверяем используемые имена
        for name in code.co_names:
            if name not in allowed_names:
                raise ValueError(f"Name '{name}' is not allowed")
        
        # Вычисляем
        return eval(code, {"__builtins__": {}}, context)
    
    def parse_coordinate(self, coord: Any, context: Dict[str, Any] = None) -> float:
        """
        Парсит координату, которая может быть числом или выражением
        """
        if isinstance(coord, (int, float)):
            return float(coord)
        elif isinstance(coord, str):
            return self.parse(coord, context)
        else:
            return 0.0