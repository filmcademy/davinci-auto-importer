import flet as ft
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send2trash import send2trash
import sys

# Add DaVinci Resolve scripting module path
if sys.platform.startswith("win"):
    resolve_script_path = os.path.join(
        os.environ.get("PROGRAMDATA", ""),
        "Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
    )
    sys.path.append(resolve_script_path)

try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    print("Failed to import DaVinciResolveScript.")
    sys.exit()

class FileHandler(FileSystemEventHandler):
    def __init__(self, app_instance):
        self.app = app_instance
        self.processed_files = set()

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path not in self.processed_files:
                self.processed_files.add(file_path)
                self.app.add_new_file(file_path)

class FolderMonitorApp:
    def __init__(self):
        self.folder_path = None
        self.observer = None
        self.file_handler = FileHandler(self)
        self.page = None

        # Initialize DaVinci Resolve scripting API
        self.resolve = dvr_script.scriptapp("Resolve")
        if not self.resolve:
            print("Failed to connect to DaVinci Resolve.")
            sys.exit()
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        if not self.project:
            print("No project is currently open in DaVinci Resolve.")
            sys.exit()
        self.media_pool = self.project.GetMediaPool()
        self.media_storage = self.resolve.GetMediaStorage()
        # Remove timeline initialization from here
        # self.current_timeline = self.project.GetCurrentTimeline()
        # if not self.current_timeline:
        #     # Create a new timeline if none exists
        #     self.current_timeline = self.media_pool.CreateEmptyTimeline("Timeline 1")
        #     if not self.current_timeline:
        #         print("Failed to create a new timeline.")
        #         sys.exit()

    def add_new_file(self, file_path):
        def handle_validate():
            print(f"Validating file: {file_path}")

            # Import the file into the media pool
            file_list = [file_path]
            print(f"Attempting to add {file_list} to media pool.")
            added_items = self.media_storage.AddItemListToMediaPool(file_list)
            if added_items:
                print("File added to media pool.")

                # Check if a timeline exists
                current_timeline = self.project.GetCurrentTimeline()
                if not current_timeline:
                    print("No timeline exists. Creating a new timeline with the added clip.")
                    # Create a new timeline using the added clip
                    new_timeline = self.media_pool.CreateTimelineFromClips("Timeline 1", added_items)
                    if new_timeline:
                        print("New timeline created successfully.")
                        self.current_timeline = new_timeline
                    else:
                        print("Failed to create a new timeline.")
                        return
                else:
                    print("Timeline exists. Appending clip to the timeline.")
                    # Append the clip to the existing timeline
                    success = self.media_pool.AppendToTimeline(added_items)
                    if success:
                        print(f"Added {file_path} to timeline.")
                    else:
                        print(f"Failed to add {file_path} to timeline.")
            else:
                print(f"Failed to add {file_path} to media pool.")

            self.page.remove(file_controls)
            self.page.update()

        def handle_trash():
            try:
                send2trash(file_path)
                self.page.remove(file_controls)
                self.page.update()
            except Exception as e:
                print(f"Error moving file to trash: {e}")

        file_controls = ft.Row(
            controls=[
                ft.Text(os.path.basename(file_path)),
                ft.ElevatedButton("Validate", on_click=lambda _: handle_validate()),
                ft.ElevatedButton("Move to Trash", on_click=lambda _: handle_trash())
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.page.add(file_controls)
        self.page.update()

    def start_monitoring(self, folder_path):
        self.folder_path = folder_path
        self.observer = Observer()
        self.observer.schedule(self.file_handler, folder_path, recursive=False)
        self.observer.start()

    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Folder Monitor"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def handle_folder_selection(e):
            if e.path:
                self.start_monitoring(e.path)
                status_text.value = f"Monitoring: {e.path}"
                page.update()

        folder_picker = ft.FilePicker(
            on_result=handle_folder_selection
        )

        page.overlay.append(folder_picker)

        status_text = ft.Text("No folder selected")

        page.add(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Select Folder",
                        on_click=lambda _: folder_picker.get_directory_path()
                    ),
                    status_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

def main():
    app = FolderMonitorApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
