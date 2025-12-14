from typing import Dict, List, Any
import pyglet

class AddonManager:
    """Централизованный менеджер аддонов"""
    
    def __init__(self):
        self.addons: Dict[str, BaseAddon] = {}
        self.batches: Dict[str, pyglet.graphics.Batch] = {}
    
    def register_addon(self, addon):
        """Регистрация аддона"""
        from addon_base import BaseAddon
        if isinstance(addon, BaseAddon):
            self.addons[addon.addon_id] = addon
            print(f"Addon '{addon.addon_id}' registered (types: {addon.supported_types})")
    
    def process_json(self, json_data: Dict[str, Any]) -> Dict[str, pyglet.graphics.Batch]:
        """Обработка JSON данных через аддоны"""
        batches = {}
        
        print(f"\nProcessing JSON data. Keys: {list(json_data.keys())}")
        
        for addon_id, addon in self.addons.items():
            print(f"\nChecking addon: {addon_id}")
            
            # Ищем данные для этого аддона
            for obj_type in addon.supported_types:
                print(f"  Looking for type: '{obj_type}'")
                
                if obj_type in json_data:
                    print(f"  ✓ Found '{obj_type}' in JSON")
                    data = json_data[obj_type]
                    
                    if addon.validate(data):
                        print(f"  ✓ Data validated successfully")
                        batch = addon.create_batch(data)
                        if batch is not None:
                            batches[addon_id] = batch
                            print(f"  ✓ Created batch for {addon_id}")
                    else:
                        print(f"  ✗ Data validation failed")
                else:
                    print(f"  ✗ Type '{obj_type}' not found in JSON")
        
        print(f"\nTotal batches created: {len(batches)}")
        self.batches = batches
        return batches