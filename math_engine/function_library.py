"""
Библиотека математических функций для паттернов
"""
import math
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class IFunction(ABC):
    """Интерфейс математической функции для паттернов"""
    
    @abstractmethod
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        """
        Вычисление функции
        
        Args:
            params: Параметры функции (angle, size, time, n и т.д.)
            
        Returns:
            Список координат [x, y]
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
        self.register(SquareFunction())  # НОВАЯ!
        self.register(FixedFunction())   # НОВАЯ!
        self.register(SpiralFunction())
        self.register(CubeFunction())
    
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
        size = params.get("size", 1.0)  # ← size вместо radius
        
        x = size * math.cos(angle)
        y = size * math.sin(angle)
        
        return [x, y]


class SquareFunction(IFunction):
    """
    Точка на квадрате, синхронизированная с кругом.
    angle=0 → (size, 0) - середина правой стороны
    """
    
    @property
    def function_id(self) -> str:
        return "square"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        angle = params.get("angle", 0.0)
        size = params.get("size", 1.0)
        
        # СМЕЩЕНИЕ: -π/4 чтобы angle=0 был на правой стороне
        angle = (angle - math.pi/4) % (2 * math.pi)
        half_pi = math.pi / 2
        
        # Определяем сторону
        side = int(angle / half_pi) % 4
        t = (angle % half_pi) / half_pi
        
        if side == 0:  # Верхняя правая -> Верхняя сторона
            x = size - 2 * size * t
            y = size
        elif side == 1:  # Верхняя левая -> Левая сторона
            x = -size
            y = size - 2 * size * t
        elif side == 2:  # Нижняя левая -> Нижняя сторона
            x = -size + 2 * size * t
            y = -size
        else:  # Нижняя правая -> Правая сторона
            x = size
            y = -size + 2 * size * t
        
        return [x, y]


class FixedFunction(IFunction):
    """Фиксированная точка (не зависит от параметров)"""
    
    @property
    def function_id(self) -> str:
        return "fixed"
    
    @property
    def required_params(self) -> List[str]:
        return ["x", "y"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        """Просто возвращает заданные координаты"""
        x = params.get("x", 0.0)
        y = params.get("y", 0.0)
        
        return [x, y]


class SpiralFunction(IFunction):
    """Функция спирали"""
    
    @property
    def function_id(self) -> str:
        return "spiral"
    
    @property
    def required_params(self) -> List[str]:
        return ["angle"]
    
    def evaluate(self, params: Dict[str, Any]) -> List[float]:
        angle = params.get("angle", 0.0)
        growth = params.get("growth", 0.1)
        base_size = params.get("base_size", 1.0)  # ← base_size вместо base_radius
        
        # Архимедова спираль: r = a + b*θ
        r = base_size + growth * angle
        
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        return [x, y]


class CubeFunction(IFunction):
    """Функция 3D куба"""
    
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
        
        # (остальной код cube функции остается)
        # ...
        
        return [x, y]  # возвращает список всех вершин