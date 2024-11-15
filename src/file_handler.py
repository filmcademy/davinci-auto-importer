from watchdog.events import FileSystemEventHandler
from send2trash import send2trash

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, app_instance):
        self.app = app_instance
        self.processed_files = set()

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path not in self.processed_files:
                self.processed_files.add(file_path)
                self.app.add_new_file(file_path)

    def move_to_trash(self, file_path):
        try:
            send2trash(file_path)
            print(f"Moved {file_path} to trash")
        except Exception as e:
            print(f"Error moving file to trash: {e}")