import json
import os

CONFIG_FILE = "converter_config.json"

class ConfigManager:
    def __init__(self):
        self.config = self.cargar_configuracion()

    def cargar_configuracion(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                return json.load(file)
        return {"output_path": "", "width": 1920, "height": 1080, "default_image": ""}

    def guardar_configuracion(self):
        with open(CONFIG_FILE, 'w') as file:
            json.dump(self.config, file)

    def get_config(self):
        return self.config
