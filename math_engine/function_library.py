"""
Библиотека математических функций
"""
import math
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class IFunction(ABC):
    """Интерфейс математической функции"""
    
    @abstractmethod
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        pass
    
    @property
    @abstractmethod
    def function_id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def required_params(self) -> List[str]:
        pass


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


class SumFunction(IFunction):
    """Сумма нескольких функций с поддержкой выражений"""
    
    def __init__(self, function_library=None, expression_parser=None):
        self.function_library = function_library
        self.expression_parser = expression_parser
    
    @property
    def function_id(self) -> str:
        return "sum"
    
    @property
    def required_params(self) -> List[str]:
        return ["functions"]
    
    def evaluate(self, params: Dict[str, Any], context: Dict[str, Any] = None) -> List[float]:
        functions = params.get("functions", [])
        
        if not functions or not self.function_library:
            return [0, 0]
        
        total_x, total_y = 0.0, 0.0
        
        for func_config in functions:
            try:
                # Парсим параметры с контекстом
                parsed_config = self._parse_config_with_context(func_config, context)
                
                func_name = parsed_config.get("func", "circle")
                func = self.function_library.get(func_name)
                
                # Вычисляем координаты с передачей контекста
                if func_name == "sum" and isinstance(func, SumFunction):
                    # Для вложенной суммы устанавливаем парсер, если его нет
                    if func.expression_parser is None:
                        func.expression_parser = self.expression_parser
                    coords = func.evaluate(parsed_config, context)
                else:
                    coords = func.evaluate(parsed_config, context)
                
                if len(coords) >= 2:
                    total_x += coords[0]
                    total_y += coords[1]
                    
            except Exception as e:
                print(f"Error in sum function: {e}")
        
        return [total_x, total_y]
    
    def _parse_config_with_context(self, config: Dict[str, Any], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Парсит параметры с использованием expression_parser и контекста"""
        if not self.expression_parser:
            return config
        
        parsed_config = config.copy()
        
        for key, value in config.items():
            if key == "func":
                continue
            
            elif key == "functions":
                # Рекурсивно парсим вложенные функции
                if isinstance(value, list):
                    parsed_functions = []
                    for func_item in value:
                        if isinstance(func_item, dict):
                            parsed_functions.append(
                                self._parse_config_with_context(func_item, context)
                            )
                        else:
                            parsed_functions.append(func_item)
                    parsed_config[key] = parsed_functions
            
            elif isinstance(value, str):
                # Парсим выражение
                try:
                    parsed_value = self.expression_parser.parse(value, context or {})
                    parsed_config[key] = parsed_value
                except Exception as e:
                    print(f"Error parsing {key}='{value}': {e}")
                    parsed_config[key] = 0.0
        
        return parsed_config