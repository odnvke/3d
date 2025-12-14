"""
Реестр математических функций
"""
from typing import Dict, Any, List
from .functions import (
    IFunction,
    CircleFunction,
    SquareFunction,
    FixedFunction,
    NGonFunction,
    SumFunction,
    MultiplyFunction,
    MorphFunction,
    DirectedLineFunction  # <-- Добавляем импорт
)


class FunctionLibrary:
    """Реестр математических функций"""
    
    def __init__(self, expression_parser=None):
        self._functions: Dict[str, IFunction] = {}
        self.expression_parser = expression_parser
        self._register_builtin_functions()
    
    def _register_builtin_functions(self):
        """Регистрация встроенных функций"""
        # Базовые функции
        self.register(CircleFunction())
        self.register(SquareFunction())
        self.register(FixedFunction())
        self.register(NGonFunction())
        
        # Композитные функции (передаём библиотеку и парсер)
        self.register(SumFunction(self, self.expression_parser))
        self.register(MultiplyFunction(self, self.expression_parser))
        self.register(MorphFunction(self, self.expression_parser))
        self.register(DirectedLineFunction(self, self.expression_parser))  # <-- Регистрируем
    
    def register(self, function: IFunction):
        self._functions[function.function_id] = function
    
    def get(self, function_id: str) -> IFunction:
        func = self._functions.get(function_id)
        if func is None:
            raise ValueError(f"Function '{function_id}' not found")
        return func
    
    def list_functions(self) -> List[str]:
        return list(self._functions.keys())
    
    def evaluate(self, function_id: str, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        func = self.get(function_id)
        return func.evaluate(params, context)