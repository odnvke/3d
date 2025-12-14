"""
Библиотека математических функций для паттернов
"""
import math
from typing import Dict, Callable, Any, List
from abc import ABC, abstractmethod


class IFunction(ABC):
    """Интерфейс математической функции для паттернов"""
    
    @abstractmethod
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        """
        Вычисление функции
        
        Args:
            params: Параметры функции (angle, radius, time, n и т.д.)
            
        Returns:
            Список координат [x, y] или [x, y, z]
        """
        pass
    
    @property
    @abstractmethod
    def function_id(self) -> str:
        """Уникальный идентификатор функции"""
        pass
    
    @property
    @abstractmethod
    def required_params(self) -> List[str]:
        """Обязательные параметры функции"""
        pass


class FunctionLibrary:
    """Реестр математических функций"""
    
    def __init__(self):
        self._functions: Dict[str, IFunction] = {}
        self._register_builtin_functions()
    
    def _register_builtin_functions(self):
        """Регистрация встроенных функций"""
        self.register(CircleFunction())
        self.register(SpiralFunction())
        self.register(CubeFunction())
        self.register(WaveFunction())
        self.register(GridFunction())
    
    def register(self, function: IFunction):
        """Регистрация новой функции"""
        self._functions[function.function_id] = function
        print(f"Function '{function.function_id}' registered")
    
    def get(self, function_id: str) -> IFunction:
        """Получение функции по идентификатору"""
        func = self._functions.get(function_id)
        if func is None:
            raise ValueError(f"Function '{function_id}' not found")
        return func
    
    def list_functions(self) -> List[str]:
        """Список всех зарегистрированных функций"""
        return list(self._functions.keys())
    
    def evaluate(self, function_id: str, params: Dict[str, Any]) -> List[float]:
        """Вычисление функции с заданными параметрами"""
        func = self.get(function_id)
        return func.evaluate(params)


class CircleFunction(IFunction):
    """Функция окружности"""
    
    @property
    def function_id(self) -> str:
        return "circle"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        angle = params.get("angle", 0.0)
        radius = params.get("radius", 1.0)
        
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        return [x, y]


class SpiralFunction(IFunction):
    """Функция спирали (Архимедова)"""
    
    @property
    def function_id(self) -> str:
        return "spiral"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        angle = params.get("angle", 0.0)
        growth = params.get("growth", 0.1)  # Коэффициент роста
        radius = params.get("base_radius", 1.0)
        
        # Архимедова спираль: r = a + b*θ
        r = radius + growth * angle
        
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        return [x, y]


class CubeFunction(IFunction):
    """Функция 3D куба (проекция на 2D)"""
    
    @property
    def function_id(self) -> str:
        return "cube"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle_x", "angle_y"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        angle_x = params.get("angle_x", 0.0)
        angle_y = params.get("angle_y", 0.0)
        size = params.get("size", 1.0)
        
        # Вершины куба в 3D
        vertices_3d = [
            [-1, -1, -1],
            [ 1, -1, -1],
            [ 1,  1, -1],
            [-1,  1, -1],
            [-1, -1,  1],
            [ 1, -1,  1],
            [ 1,  1,  1],
            [-1,  1,  1]
        ]
        
        # Матрицы поворота
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        
        # Поворачиваем и проецируем
        result = []
        for vertex in vertices_3d:
            x, y, z = vertex
            
            # Поворот вокруг оси Y
            x1 = x * cos_y - z * sin_y
            z1 = x * sin_y + z * cos_y
            
            # Поворот вокруг оси X
            y1 = y * cos_x - z1 * sin_x
            z2 = y * sin_x + z1 * cos_x
            
            # Ортографическая проекция (игнорируем Z)
            x_proj = x1 * size
            y_proj = y1 * size
            
            result.extend([x_proj, y_proj])
        
        return result


class WaveFunction(IFunction):
    """Волновая функция (синусоида)"""
    
    @property
    def function_id(self) -> str:
        return "wave"
    
    @property
    def required_params(self) -> List[str]:
        return ["x"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        x = params.get("x", 0.0)
        amplitude = params.get("amplitude", 1.0)
        frequency = params.get("frequency", 1.0)
        phase = params.get("phase", 0.0)
        
        y = amplitude * math.sin(frequency * x + phase)
        
        return [x, y]


class GridFunction(IFunction):
    """Сеточная функция"""
    
    @property
    def function_id(self) -> str:
        return "grid"
    
    @property
    def required_params(self) -> List[str]:
        return ["u", "v"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        u = params.get("u", 0.0)
        v = params.get("v", 0.0)
        cell_size = params.get("cell_size", 1.0)
        
        x = u * cell_size
        y = v * cell_size
        
        return [x, y]