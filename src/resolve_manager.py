import os
import sys

class ResolveManager:
    def __init__(self):
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
            # Try both possible Linux paths
            standard_path = "/opt/resolve/Developer/Scripting/Modules/"
            alt_path = "/home/resolve/Developer/Scripting/Modules/"
            resolve_script_path = standard_path if os.path.exists(standard_path) else alt_path
        else:
            print(f"Unsupported operating system: {sys.platform}")
            sys.exit(1)

        if resolve_script_path not in sys.path:
            sys.path.append(resolve_script_path)
        
        try:
            import DaVinciResolveScript as dvr_script
        except ImportError:
            print("Error: Could not import DaVinci Resolve scripting module.")
            print(f"Please verify that DaVinci Resolve is installed and the scripting API is enabled.")
            print(f"Looking for module in: {resolve_script_path}")
            sys.exit(1)

        self.resolve = dvr_script.scriptapp("Resolve")
        if not self.resolve:
            print("Failed to connect to DaVinci Resolve.")
            sys.exit(1)
            
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        if not self.project:
            print("No project is currently open in DaVinci Resolve.")
            sys.exit(1)
            
        self.media_pool = self.project.GetMediaPool()
        self.media_storage = self.resolve.GetMediaStorage()

    def process_file(self, file_path):
        print(f"Validating file: {file_path}")
        file_list = [file_path]
        print(f"Attempting to add {file_list} to media pool.")
        
        added_items = self.media_storage.AddItemListToMediaPool(file_list)
        if not added_items:
            print(f"Failed to add {file_path} to media pool.")
            return

        print("File added to media pool.")
        current_timeline = self.project.GetCurrentTimeline()
        
        if not current_timeline:
            print("No timeline exists. Creating a new timeline with the added clip.")
            new_timeline = self.media_pool.CreateTimelineFromClips("Timeline 1", added_items)
            if new_timeline:
                print("New timeline created successfully.")
            else:
                print("Failed to create a new timeline.")
                return
        else:
            print("Timeline exists. Appending clip to the timeline.")
            success = self.media_pool.AppendToTimeline(added_items)
            if success:
                print(f"Added {file_path} to timeline.")
            else:
                print(f"Failed to add {file_path} to timeline.")