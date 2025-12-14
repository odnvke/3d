import pyglet
from typing import Dict, Any, Optional, List
from addon_base import BaseAddon

class LinesAddon(BaseAddon):
    """Аддон для рисования линий (упрощенный для Pyglet 2.x)"""
    
    def __init__(self):
        self.lines = []
    
    @property
    def addon_id(self) -> str:
        return "lines"
    
    @property
    def supported_types(self) -> list:
        return ["lines", "line", "segments"]
    
    def validate(self, data: Any) -> bool:
        return isinstance(data, list)
    
    def create_batch(self, data: List[Dict[str, Any]], batch: Optional[pyglet.graphics.Batch] = None) -> pyglet.graphics.Batch:
        """Создание линий"""
        if batch is None:
            batch = pyglet.graphics.Batch()
        
        print(f"LinesAddon: Creating {len(data)} lines")
        self.lines = []  # Очищаем список
        
        for i, line_def in enumerate(data):
            try:
                start = line_def.get('start', [100, 100])
                end = line_def.get('end', [200, 200])
                color = line_def.get('color', [255, 0, 0])
                
                if len(color) == 3:
                    color = tuple(color[:3])
                elif len(color) == 4:
                    color = tuple(color[:3])
                
                print(f"  Line {i}: {start} -> {end}")
                
                # Просто используем shapes.Line - он работает в batch
                line = pyglet.shapes.Line(
                    start[0], start[1],
                    end[0], end[1],
                    color=color,
                    batch=batch
                )
                
                self.lines.append(line)
                
            except Exception as e:
                print(f"  Error creating line {i}: {e}")
        
        return batch
    
    def draw(self, batch: pyglet.graphics.Batch):
        """Отрисовка линий"""
        # Устанавливаем толщину линии (если нужно)
        pyglet.gl.glLineWidth(2.0)
        batch.draw()
        pyglet.gl.glLineWidth(1.0)