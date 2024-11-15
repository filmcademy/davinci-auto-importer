import flet as ft
from watchdog.observers import Observer
import os

class UIManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.page = None
        self.status_text = None
        self.observer = None

    def initialize_page(self, page: ft.Page):
        self.page = page
        self.page.title = "Folder Monitor"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.status_text = ft.Text("No folder selected")
        
    def setup_folder_picker(self):
        folder_picker = ft.FilePicker(
            on_result=self._handle_folder_selection
        )
        
        self.page.overlay.append(folder_picker)
        
        self.page.add(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Select Folder",
                        on_click=lambda _: folder_picker.get_directory_path()
                    ),
                    self.status_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def _handle_folder_selection(self, e):
        if e.path:
            self._start_monitoring(e.path)
            self.status_text.value = f"Monitoring: {e.path}"
            self.page.update()

    def _start_monitoring(self, folder_path):
        self.observer = Observer()
        self.observer.schedule(self.app.file_handler, folder_path, recursive=False)
        self.observer.start()

    def create_file_controls(self, file_path, validate_callback, trash_callback):
        file_controls = ft.Row(
            controls=[
                ft.Text(os.path.basename(file_path)),
                ft.ElevatedButton("Validate", on_click=lambda _: self._handle_validate(validate_callback, file_controls)),
                ft.ElevatedButton("Move to Trash", on_click=lambda _: self._handle_trash(trash_callback, file_controls))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.page.add(file_controls)
        self.page.update()

    def _handle_validate(self, callback, controls):
        callback()
        self.page.remove(controls)
        self.page.update()

    def _handle_trash(self, callback, controls):
        callback()
        self.page.remove(controls)
        self.page.update()