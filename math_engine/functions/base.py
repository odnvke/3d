"""
Базовый интерфейс функции
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


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