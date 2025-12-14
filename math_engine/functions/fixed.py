"""
Фиксированная точка
"""
from typing import Dict, Any, List
from .base import IFunction


class FixedFunction(IFunction):
    """Фиксированная точка"""
    
    @property
    def function_id(self) -> str:
        return "fixed"
    
    @property
    def required_params(self) -> List[str]:
        return ["x", "y"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        x = float(params.get("x", 0.0))
        y = float(params.get("y", 0.0))
        return [x, y]