import pyglet
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAddon(ABC):
    """Абстрактный базовый класс для всех аддонов"""
    
    @property
    @abstractmethod
    def addon_id(self) -> str:
        """Уникальный ID аддона"""
        pass
    
    @property
    @abstractmethod
    def supported_types(self) -> list:
        """Типы объектов, которые обрабатывает аддон"""
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Валидация входных данных"""
        pass
    
    @abstractmethod
    def create_batch(self, data: Any, batch: Optional[pyglet.graphics.Batch] = None) -> pyglet.graphics.Batch:
        """Создание графических объектов"""
        pass