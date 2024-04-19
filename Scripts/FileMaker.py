"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import CaptionManager
from importlib import reload

reload(CaptionManager)

from ProToolsMarkers import ProToolsMarkerManager

class FileMaker:
    def __init__(self, timecode_filename: str):
        self.marker_manager = ProToolsMarkerManager(timecode_filename)
        self.script_manager = None


    """
    Read through markers and call the function provided by the caller
    update_file:    Function to call
    """
    def read_through_markers(self, update_file) -> None:
        # Get the first markers
        next_marker = self.marker_manager.get_next_marker()

        while True:
            marker = next_marker
            while marker is not None and self.skip_marker(marker.name):
                marker = self.marker_manager.get_next_marker()
            next_marker = self.marker_manager.get_next_marker()
            while next_marker is not None and self.skip_marker(next_marker.name, True):
                next_marker = self.marker_manager.get_next_marker()
            
            # If no more markers, break
            if marker is None or next_marker is None:
                break
            
            # Call the function provided by the caller
            update_file(self, marker, next_marker)

        return


    """
    Logic to skip markers
    name:           Marker name
    is_end:         Is the marker the last marker in the script
    """
    def skip_marker(self, name: str, is_end: bool = False) -> bool:
        if is_end:
            return False
        return (name == 'x' or name == 'END')

