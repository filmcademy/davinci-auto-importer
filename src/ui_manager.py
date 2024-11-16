import flet as ft
from watchdog.observers import Observer
import os

class UIManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.page = None
        self.status_text = None
        self.observer = None
        self.files_column = None
        self.connection_status = None
        self.refresh_button = None
        self.connection_row = None

    def initialize_page(self, page: ft.Page):
        self.page = page
        self.page.title = "DaVinci Resolve Auto-Import"
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 600
        self.page.window_height = 800
        self.page.window_min_width = 400
        self.page.window_min_height = 600
        
        # Create a container for file items
        self.files_column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Initialize status text with styling
        self.status_text = ft.Text(
            "No folder selected",
            size=16,
            color=ft.colors.GREY_500,
            text_align=ft.TextAlign.CENTER,
        )

        # Add connection status and refresh button
        self.connection_status = ft.Text(
            "⚠️ DaVinci Resolve is not running",
            size=16,
            color=ft.colors.ORANGE_400,
            text_align=ft.TextAlign.CENTER,
        )

        self.refresh_button = ft.IconButton(
            icon=ft.icons.REFRESH,
            tooltip="Check DaVinci Resolve Connection",
            on_click=self._check_resolve_connection
        )

        self.connection_row = ft.Row(
            [self.connection_status, self.refresh_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def setup_folder_picker(self):
        folder_picker = ft.FilePicker(
            on_result=self._handle_folder_selection
        )
        
        self.page.overlay.append(folder_picker)
        
        # Create header with logo/title
        header = ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.MOVIE_FILTER_ROUNDED, size=64, color=ft.colors.BLUE_400),
                ft.Text("DaVinci Resolve Auto-Import", size=24, weight=ft.FontWeight.BOLD),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            margin=ft.margin.only(bottom=20),
        )

        # Create select folder button with icon
        select_folder_btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.FOLDER_OPEN),
                    ft.Text("Select Folder", size=16),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                padding=ft.padding.all(20),
            ),
            on_click=lambda _: folder_picker.get_directory_path()
        )

        # Update the main content layout to include connection status
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        header,
                        self.connection_row,  # Add connection status and refresh button
                        select_folder_btn,
                        self.status_text,
                        ft.Divider(height=2, color=ft.colors.GREY_700),
                        ft.Text("Monitored Files:", size=16, weight=ft.FontWeight.BOLD),
                        self.files_column,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )

    def create_file_controls(self, file_path, validate_callback, trash_callback):
        file_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.VIDEO_FILE, color=ft.colors.BLUE_400),
                        title=ft.Text(os.path.basename(file_path), size=16),
                        subtitle=ft.Text(
                            os.path.dirname(file_path),
                            size=12,
                            color=ft.colors.GREY_400,
                            no_wrap=True,
                            max_lines=1,
                        ),
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.CHECK_CIRCLE_OUTLINE,
                                icon_color=ft.colors.GREEN_400,
                                tooltip="Validate",
                                on_click=lambda _: self._handle_validate(validate_callback, file_card),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_color=ft.colors.RED_400,
                                tooltip="Move to Trash",
                                on_click=lambda _: self._handle_trash(trash_callback, file_card),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]),
                padding=10,
            ),
        )
        
        self.files_column.controls.insert(0, file_card)
        self.page.update()

    def _handle_folder_selection(self, e):
        if e.path:
            self._start_monitoring(e.path)
            self.status_text.value = f"Monitoring: {e.path}"
            self.status_text.color = ft.colors.GREEN_400
            self.page.update()

    def _handle_validate(self, callback, controls):
        callback()
        self.files_column.controls.remove(controls)
        self.page.update()

    def _handle_trash(self, callback, controls):
        callback()
        self.files_column.controls.remove(controls)
        self.page.update()

    def _start_monitoring(self, folder_path):
        self.observer = Observer()
        self.observer.schedule(self.app.file_handler, folder_path, recursive=False)
        self.observer.start()

    def _check_resolve_connection(self, _):
        if self.app.resolve_manager.try_connect():
            self.connection_status.value = "✅ Connected to DaVinci Resolve"
            self.connection_status.color = ft.colors.GREEN_400
        else:
            self.connection_status.value = "⚠️ DaVinci Resolve is not running"
            self.connection_status.color = ft.colors.ORANGE_400
        self.page.update()