#!/usr/bin/env python3
"""
Главный файл приложения для параметрических линий
"""

from core import LineDrawerApp
from addon_lines import LinesAddon
from addon_parametric import ParametricLinesAddon
# from addon_shapes import ShapesAddon


def main():
    # Создаем приложение
    app = LineDrawerApp("example_parametric.json", width=1024, height=768)
    
    # Регистрируем аддоны
    app.register_addon(LinesAddon())
    app.register_addon(ParametricLinesAddon())  # Параметрические линии
    #app.register_addon(ShapesAddon())
    
    # Запускаем
    app.run()


if __name__ == "__main__":
    main()