"""
Паттерн 3D куба - проекция вращающегося куба
"""
import math
from typing import Tuple, Dict, Any, List
from .base_pattern import BasePattern


class CubePattern(BasePattern):
    """Паттерн 3D куба (12 линий = 12 ребер куба)"""
    
    @property
    def pattern_id(self) -> str:
        return "cube"
    
    def get_line_count(self) -> int:
        """У куба всегда 12 ребер"""
        return 12
    
    def calculate_line(self, n: int, time: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Вычисление координат для ребра n 3D куба
        """
        # Вершины куба в локальных координатах
        vertices = [
            (-1, -1, -1),  # 0
            (1, -1, -1),   # 1
            (1, 1, -1),    # 2
            (-1, 1, -1),   # 3
            (-1, -1, 1),   # 4
            (1, -1, 1),    # 5
            (1, 1, 1),     # 6
            (-1, 1, 1)     # 7
        ]
        
        # Ребра куба (пары индексов вершин)
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Нижняя грань
            (4, 5), (5, 6), (6, 7), (7, 4),  # Верхняя грань
            (0, 4), (1, 5), (2, 6), (3, 7)   # Вертикальные ребра
        ]
        
        # Получаем параметры
        center_x = self.config.get('center_x', 0.0)
        center_y = self.config.get('center_y', 0.0)
        size = self.config.get('size', 100.0)
        
        # Углы вращения
        if self.expression_parser:
            context = {'n': n, 'time': time, 'count': 12}
            angle_x = self.expression_parser.parse(
                self.config.get('angle_x_expression', 'time*0.5'),
                context
            )
            angle_y = self.expression_parser.parse(
                self.config.get('angle_y_expression', 'time*0.3'),
                context
            )
            angle_z = self.expression_parser.parse(
                self.config.get('angle_z_expression', '0'),
                context
            )
        else:
            angle_x = time * 0.5
            angle_y = time * 0.3
            angle_z = 0.0
        
        # Получаем индексы вершин для этого ребра
        if n < len(edges):
            v1_idx, v2_idx = edges[n]
        else:
            v1_idx, v2_idx = edges[0]
        
        # Получаем координаты вершин
        v1 = self._rotate_vertex(vertices[v1_idx], angle_x, angle_y, angle_z)
        v2 = self._rotate_vertex(vertices[v2_idx], angle_x, angle_y, angle_z)
        
        # Масштабируем и сдвигаем
        start_x = center_x + v1[0] * size
        start_y = center_y + v1[1] * size
        end_x = center_x + v2[0] * size
        end_y = center_y + v2[1] * size
        
        return ((start_x, start_y), (end_x, end_y))
    
    def _rotate_vertex(self, vertex, angle_x, angle_y, angle_z):
        """Вращение 3D вершины"""
        x, y, z = vertex
        
        # Вращение вокруг оси X
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x
        
        # Вращение вокруг оси Y
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        x1 = x * cos_y + z1 * sin_y
        z2 = -x * sin_y + z1 * cos_y
        
        # Вращение вокруг оси Z
        cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
        x2 = x1 * cos_z - y1 * sin_z
        y2 = x1 * sin_z + y1 * cos_z
        
        # Ортографическая проекция (игнорируем Z)
        return (x2, y2)