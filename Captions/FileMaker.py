"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

from ProToolsData.ProToolsDataManager import ProToolsDataManager
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# ================================================================================================

class FileMaker:
    # ----------------------------------------------------------------------------
    # FileMaker
    # timecode_filename: str    - the name of the file containing the timecode data
    def __init__(self, timecode_filename: str, data_type: str = "MRK"):
        self.data_manager = ProToolsDataManager.from_file(timecode_filename, data_type)
        self.script_manager = None
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Read through markers and call the function provided by the caller
    # update_file:    Function to call
    ## returns: bool
    def read_through_markers(self, update_file) -> bool:

        while True:
            node = self.data_manager.get_current_node()
            if node == None:
                break
            
            marker = node.marker
            end_marker = node.get_end()

            # If no more markers, break
            if marker == None or end_marker == None:
                break
            
            logging.debug(f"Marker: {marker.name}\t\t{marker.timecode.get_timecode_in_frames()}")

            # Call the function provided by the caller
            update_file(self, marker, end_marker)

        return True
    # ----------------------------------------------------------------------------

# ================================================================================================