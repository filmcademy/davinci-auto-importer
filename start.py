import flet as ft
from src.ui_manager import UIManager
from src.file_handler import FileEventHandler
from src.resolve_manager import ResolveManager

class AutoImportApp:
    def __init__(self):
        self.resolve_manager = ResolveManager()
        self.file_handler = FileEventHandler(self)
        self.ui_manager = UIManager(self)

    def add_new_file(self, file_path):
        def validate_callback():
            self.resolve_manager.process_file(file_path)

        def trash_callback():
            self.file_handler.move_to_trash(file_path)

        self.ui_manager.create_file_controls(
            file_path, 
            validate_callback, 
            trash_callback
        )

    def main(self, page: ft.Page):
        self.ui_manager.initialize_page(page)
        self.ui_manager.setup_folder_picker()

def main():
    app = AutoImportApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
