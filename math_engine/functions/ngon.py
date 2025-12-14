"""
Функция N-угольника
"""
import math
from typing import Dict, Any, List
from .base import IFunction


class NGonFunction(IFunction):
    """Функция N-угольника"""
    
    @property
    def function_id(self) -> str:
        return "ngon"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        angle = float(params.get("angle", 0.0))
        size = float(params.get("size", 1.0))
        sides = float(params.get("sides", 5.0))
        rotation = float(params.get("rotation", 0.0))
        
        angle = angle + rotation
        
        if sides < 3:
            sides = 3
        
        sides_int = int(math.floor(sides))
        sides_frac = sides - sides_int
        
        if sides_frac < 0.001:
            return self._point_on_ngon(angle, size, sides_int)
        else:
            point1 = self._point_on_ngon(angle, size, sides_int)
            point2 = self._point_on_ngon(angle, size, sides_int + 1)
            
            x = point1[0] + sides_frac * (point2[0] - point1[0])
            y = point1[1] + sides_frac * (point2[1] - point1[1])
            
            return [x, y]
    
    def _point_on_ngon(self, angle: float, size: float, sides_int: int) -> List[float]:
        side_angle = 2 * math.pi / sides_int
        
        adjusted_angle = (angle - side_angle/2) % (2 * math.pi)
        side_index = int(adjusted_angle / side_angle) % sides_int
        t = (adjusted_angle % side_angle) / side_angle
        
        vertices = []
        for i in range(sides_int):
            vertex_angle = i * side_angle + side_angle/2
            x = size * math.cos(vertex_angle)
            y = size * math.sin(vertex_angle)
            vertices.append((x, y))
        
        vertices.append(vertices[0])
        
        x1, y1 = vertices[side_index]
        x2, y2 = vertices[side_index + 1]
        
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        
        return [x, y]