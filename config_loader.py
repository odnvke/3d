import json
from typing import Dict, Any


class ConfigLoader:
    """Загрузка и парсинг JSON конфигурации"""
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Загрузка JSON из файла"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"ConfigLoader: Successfully loaded {filepath}")
                return data
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {}
    
    @staticmethod
    def validate_structure(data: Dict[str, Any]) -> bool:
        """Базовая валидация структуры"""
        if not isinstance(data, dict):
            return False
        return True