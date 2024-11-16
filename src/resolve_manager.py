import os
import sys

class ResolveManager:
    def __init__(self):
        self.resolve = None
        self.project_manager = None
        self.project = None
        self.media_pool = None
        self.media_storage = None
        self.is_connected = False
        self._initialize_resolve()
        
    def _initialize_resolve(self):
        # Add DaVinci Resolve scripting module path based on OS
        if sys.platform.startswith("win"):
            resolve_script_path = os.path.join(
                os.environ.get("PROGRAMDATA", ""),
                "Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
            )
        elif sys.platform.startswith("darwin"):  # macOS
            resolve_script_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("linux"):
            standard_path = "/opt/resolve/Developer/Scripting/Modules/"
            alt_path = "/home/resolve/Developer/Scripting/Modules/"
            resolve_script_path = standard_path if os.path.exists(standard_path) else alt_path
        else:
            print(f"Unsupported operating system: {sys.platform}")
            return False

        if resolve_script_path not in sys.path:
            sys.path.append(resolve_script_path)
        
        try:
            import DaVinciResolveScript as dvr_script
        except ImportError:
            print("Error: Could not import DaVinci Resolve scripting module.")
            return False

        try:
            self.resolve = dvr_script.scriptapp("Resolve")
            if not self.resolve:
                return False
                
            self.project_manager = self.resolve.GetProjectManager()
            self.project = self.project_manager.GetCurrentProject()
            if not self.project:
                return False
                
            self.media_pool = self.project.GetMediaPool()
            self.media_storage = self.resolve.GetMediaStorage()
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Error connecting to DaVinci Resolve: {e}")
            return False

    def try_connect(self):
        """Attempt to connect to DaVinci Resolve"""
        return self._initialize_resolve()

    def process_file(self, file_path):
        if not self.is_connected:
            print("Not connected to DaVinci Resolve")
            return False
            
        print(f"Validating file: {file_path}")
        file_list = [file_path]
        print(f"Attempting to add {file_list} to media pool.")
        
        added_items = self.media_storage.AddItemListToMediaPool(file_list)
        if not added_items:
            print(f"Failed to add {file_path} to media pool.")
            return False

        print("File added to media pool.")
        current_timeline = self.project.GetCurrentTimeline()
        
        if not current_timeline:
            print("No timeline exists. Creating a new timeline with the added clip.")
            new_timeline = self.media_pool.CreateTimelineFromClips("Timeline 1", added_items)
            if new_timeline:
                print("New timeline created successfully.")
                return True
            else:
                print("Failed to create a new timeline.")
                return False
        else:
            print("Timeline exists. Appending clip to the timeline.")
            success = self.media_pool.AppendToTimeline(added_items)
            if success:
                print(f"Added {file_path} to timeline.")
                return True
            else:
                print(f"Failed to add {file_path} to timeline.")
                return False