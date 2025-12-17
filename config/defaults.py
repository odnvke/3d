"""
Стандартные значения
"""
from typing import Dict, Any


class DefaultsManager:
    """Управление стандартными значениями"""
    
    GLOBAL_DEFAULTS = {
        "count": 36,
        "size": 100,
        "center": [400, 300],
        "time_factor": 0.25,
        "color": [255, 255, 255],
    }
    
    FUNCTION_DEFAULTS = {
        "circle": {
            "size": 100,
            "angle": "n * angle_step"
        },
        "square": {
            "size": 100,
            "angle": "n * angle_step"
        },
        "ngon": {
            "size": 100,
            "sides": 5,
            "angle": "n * angle_step"
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
        
        for key, default_value in cls.GLOBAL_DEFAULTS.items():
            if key not in result:
                result[key] = default_value
        
        if result.get('pattern') == 'connect' and 'points' in result:
            for point_config in result['points']:
                func_name = point_config.get('func', 'circle')
                if func_name in cls.FUNCTION_DEFAULTS:
                    for key, default_value in cls.FUNCTION_DEFAULTS[func_name].items():
                        if key not in point_config:
                            point_config[key] = default_value
        
        return result