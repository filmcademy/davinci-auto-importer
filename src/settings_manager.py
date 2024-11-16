import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"
        self.settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                return {"last_folder": None}
        return {"last_folder": None}

    def save_last_folder(self, folder_path):
        self.settings["last_folder"] = folder_path
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def get_last_folder(self):
        return self.settings.get("last_folder")