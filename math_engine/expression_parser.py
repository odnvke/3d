"""
Парсер математических выражений с поддержкой pow
"""
import math
from typing import Dict, Any


class ExpressionParser:
    """Безопасный парсер математических выражений"""
    
    def __init__(self):
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Настройка встроенных математических функций"""
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
            'atan2': math.atan2,
            
            # Степени и корни
            'pow': math.pow,      # ← ДОБАВИЛИ pow
            'sqrt': math.sqrt,
            'exp': math.exp,
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
            
            # Округление и модуль
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
            'trunc': math.trunc,

            'max': max,
            'min': min,
            
            # Другие
            'degrees': math.degrees,
            'radians': math.radians,
            'hypot': math.hypot,

            'triangle': self._triangle_oscillator,

            
        }
    
    def parse(self, expression: str, context: Dict[str, Any] = None) -> float:
        """
        Парсит и вычисляет математическое выражение
        """
        if context is None:
            context = {}
        
        try:
            # Если expression уже число
            if isinstance(expression, (int, float)):
                return float(expression)
            
            # Иначе парсим строку
            expr = expression.strip()
            if not expr:
                return 0.0
            
            # Добавляем angle_step автоматически
            if 'count' in context and context['count'] > 0:
                context['angle_step'] = 2 * math.pi / context['count']
            
            # Создаем контекст для eval
            eval_context = {
                '__builtins__': {},
                **self.builtins,
                **context
            }
            
            # Безопасное вычисление
            code = compile(expr, "<string>", "eval")
            
            # Проверяем используемые имена
            for name in code.co_names:
                if name not in eval_context:
                    raise ValueError(f"Name '{name}' is not allowed")
            
            result = eval(code, eval_context)
            return float(result)
            
        except Exception as e:
            print(f"Error parsing expression '{expression}': {e}")
            return 0.0
    
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

    def _triangle_oscillator(self, x: float, period: float = 2*math.pi) -> float:
        """
        Треугольная волна
        
        Args:
            x: входное значение
            period: период волны
            
        Returns:
            Значение от -1 до 1
        """
        if period == 0:
            return 0
        t = (x % period) / period
        if t < 0.5:
            return 4 * t - 1  # от -1 до 1
        else:
            return 3 - 4 * t  # от 1 до -1