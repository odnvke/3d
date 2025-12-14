"""
Функция окружности
"""
import math
from typing import Dict, Any, List
from .base import IFunction


class CircleFunction(IFunction):
    """Функция окружности"""
    
    @property
    def function_id(self) -> str:
        return "circle"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        angle = float(params.get("angle", 0.0))
        size = float(params.get("size", 1.0))
        rotation = float(params.get("rotation", 0.0))
        
        angle = angle + rotation
        
        x = size * math.cos(angle)
        y = size * math.sin(angle)
        
        return [x, y]