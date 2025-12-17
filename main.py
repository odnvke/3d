#!/usr/bin/env python3
"""
Главный файл приложения для параметрических линий
"""

from core import LineDrawerApp
from addon_lines import LinesAddon
from addon_parametric import ParametricLinesAddon


def main():
    # Создаем приложение
    app = LineDrawerApp("example_parametric.json", width=1024, height=768)
    
    # Создаем коллбэк для получения центра окна
    def get_window_center():
        return app.window_center
    
    # Регистрируем аддоны
    app.register_addon(LinesAddon())
    
    # Передаем коллбэк в параметрический аддон
    parametric_addon = ParametricLinesAddon(window_center_callback=get_window_center)
    app.register_addon(parametric_addon)
    
    # Запускаем
    app.run()


if __name__ == "__main__":
    main()