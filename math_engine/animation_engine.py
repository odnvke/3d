"""
Движок анимации для управления временем и интерполяцией
"""
import time
from typing import Dict, Any, Callable, Optional


class AnimationEngine:
    """Управление временем анимации и интерполяцией"""
    
    def __init__(self):
        self.start_time = time.time()
        self.current_time = 0.0
        self.time_scale = 1.0
        self.paused = False
        self.last_update_time = time.time()
        self.time_update_callbacks = []
    
    def update(self):
        """Обновление текущего времени"""
        if not self.paused:
            now = time.time()
            elapsed = now - self.last_update_time
            self.current_time += elapsed * self.time_scale
            self.last_update_time = now
            
            for callback in self.time_update_callbacks:
                callback(self.current_time)
    
    def get_time(self) -> float:
        """Получение текущего времени"""
        return self.current_time
    
    def set_time_scale(self, scale: float):
        """Установка множителя времени"""
        self.time_scale = max(0.0, scale)
    
    def pause(self):
        """Пауза анимации"""
        self.paused = True
    
    def resume(self):
        """Возобновление анимации"""
        self.paused = False
        self.last_update_time = time.time()
    
    def toggle_pause(self):
        """Переключение паузы"""
        if self.paused:
            self.resume()
        else:
            self.pause()
    
    def reset(self):
        """Сброс времени"""
        self.current_time = 0.0
        self.last_update_time = time.time()
    
    def add_time_callback(self, callback: Callable[[float], None]):
        """Добавление callback'а при обновлении времени"""
        self.time_update_callbacks.append(callback)
    
    def remove_time_callback(self, callback: Callable[[float], None]):
        """Удаление callback'а"""
        if callback in self.time_update_callbacks:
            self.time_update_callbacks.remove(callback)
