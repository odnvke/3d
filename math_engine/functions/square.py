"""
Функция квадрата
"""
import math
from typing import Dict, Any, List
from .base import IFunction


class SquareFunction(IFunction):
    """Функция квадрата"""
    
    @property
    def function_id(self) -> str:
        return "square"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        angle = float(params.get("angle", 0.0))
        size = float(params.get("size", 1.0))
        rotation = float(params.get("rotation", 0.0))
        
        angle = angle + rotation
        
        angle = (angle - math.pi/4) % (2 * math.pi)
        half_pi = math.pi / 2
        
        side = int(angle / half_pi) % 4
        t = (angle % half_pi) / half_pi
        
        if side == 0:
            x = size - 2 * size * t
            y = size
        elif side == 1:
            x = -size
            y = size - 2 * size * t
        elif side == 2:
            x = -size + 2 * size * t
            y = -size
        else:
            x = size
            y = -size + 2 * size * t
        
        return [x, y]