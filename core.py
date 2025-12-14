import pyglet
from typing import Dict, Any
from addon_manager import AddonManager
from config_loader import ConfigLoader


class LineDrawerApp:
    """Основной класс приложения с поддержкой анимации"""
    
    def __init__(self, config_file: str, width: int = 800, height: int = 600):
        self.config_file = config_file
        self.width = width
        self.height = height
        self.addon_manager = AddonManager()
        self.batches = {}
        self.update_interval = 1/60  # 60 FPS
        
        # Создаем окно
        self.window = pyglet.window.Window(
            width, height, 
            "Parametric Line Drawer", 
            resizable=True
        )
        
        # Настраиваем события
        self.setup_events()
        
        # Загружаем конфигурацию сразу
        self.load_config()
        
        # Запускаем таймер для обновления анимации
        pyglet.clock.schedule_interval(self.update, self.update_interval)
    
    def setup_events(self):
        """Настройка обработчиков событий"""
        
        @self.window.event
        def on_draw():
            # Черный фон
            pyglet.gl.glClearColor(0, 0, 0, 1)
            self.window.clear()
            self.draw()
        
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.R:
                print("\n=== Reloading configuration ===")
                self.load_config()
            elif symbol == pyglet.window.key.ESCAPE:
                self.window.close()
            elif symbol == pyglet.window.key.F:
                self.window.set_fullscreen(not self.window.fullscreen)
        
        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            print(f"Mouse click at ({x:.0f}, {y:.0f})")
    
    def register_addon(self, addon):
        """Регистрация аддона"""
        self.addon_manager.register_addon(addon)
    
    def load_config(self):
        """Загрузка и применение конфигурации"""
        print(f"\nLoading configuration from {self.config_file}")
        data = ConfigLoader.load_json(self.config_file)
        
        if data:
            # Обрабатываем все данные
            self.batches = self.addon_manager.process_json(data)
            print(f"Created {len(self.batches)} batches")
        else:
            print("Failed to load configuration")
            self.batches = {}
    
    def update(self, dt):
        """Обновление состояния для анимации"""
        pass  # Анимация обновляется в аддонах
    
    def draw(self):
        """Отрисовка всех элементов"""
        if self.batches:
            for batch_name, batch in self.batches.items():
                try:
                    # Проверяем, есть ли у аддона специальный метод draw
                    addon = self.addon_manager.addons.get(batch_name)
                    if hasattr(addon, 'draw'):
                        addon.draw(batch)
                    else:
                        batch.draw()
                except Exception as e:
                    print(f"Error drawing batch {batch_name}: {e}")
    
    def run(self):
        """Запуск приложения"""
        print("\n" + "="*50)
        print("Parametric JSON Line Drawer")
        print("Controls:")
        print("  R - reload config")
        print("  ESC - exit")
        print("  F - fullscreen")
        print("="*50)
        
        pyglet.app.run()