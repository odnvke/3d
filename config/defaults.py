"""
Стандартные значения - обновленные с size вместо radius
"""
from typing import Dict, Any, List


class DefaultsManager:
    """Управление стандартными значениями"""
    
    # Глобальные стандарты
    GLOBAL_DEFAULTS = {
        "count": 36,
        "size": 100,           # ← заменили radius на size
        "center": [400, 300],
        "time_factor": 0.3,
        "angle_step": 0.1,
        "phase_shift": 0.25,
        "color": [255, 255, 255],
        "line_width": 1
    }
    
    # Стандарты для конкретных функций
    FUNCTION_DEFAULTS = {
        "circle": {
            "size": 100,       # ← заменили radius на size
            "angle": "time + n"
        },
        "square": {
            "size": 100,       # ← заменили radius на size
            "angle": "time + 0.25 + n"
        },
        "fixed": {
            "x": 0,
            "y": 0
        }
    }
    
    @classmethod
    def apply_defaults(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """Применение стандартных значений"""
        result = config.copy()
        
        # Применяем глобальные стандарты
        for key, default_value in cls.GLOBAL_DEFAULTS.items():
            if key not in result:
                result[key] = default_value
        
        # Для паттерна connect обрабатываем points
        if result.get('pattern') == 'connect' and 'points' in result:
            for point_config in result['points']:
                func_name = point_config.get('func', 'circle')
                if func_name in cls.FUNCTION_DEFAULTS:
                    for key, default_value in cls.FUNCTION_DEFAULTS[func_name].items():
                        if key not in point_config:
                            point_config[key] = default_value
        
        return result