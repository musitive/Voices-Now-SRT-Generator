"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

from ProToolsData.ProToolsMarkerManager import ProToolsMarkerManager
from ProToolsData.ProToolsEDLManager import ProToolsEDLManager
from Scripts.ScriptManager import LdsScriptManager
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# ================================================================================================

class FileMaker:
    # ----------------------------------------------------------------------------
    # FileMaker
    # script_filename: str      - the name of the file containing the script data
    # timecode_filename: str    - the name of the file containing the timecode data
    # final_filename: str       - the name of the final file to create
    # data_type: str            - the type of data to create
    def __init__(self, script_filename: str, timecode_filename: str, final_filename: str, data_type: str = "MRK"):
        self.script_manager = LdsScriptManager(script_filename)
        self.final_filename = final_filename
        self.data_type = data_type

        if timecode_filename is not None:
            assert data_type in SUPPORTED_DATA_TYPES_INIT, f"Error: Invalid data type: {data_type}"

            initializer = SUPPORTED_DATA_TYPES_INIT[data_type]
            self.data_manager = initializer.from_file(timecode_filename)
    
        elif self.script_manager.has_timecodes():
            timecode_dict = self.script_manager.get_timecodes()
            self.data_manager = ProToolsMarkerManager.from_script(timecode_dict)
            
        else:
            raise Exception("No timecode file provided and no timecodes found in script file")
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # TO OVERRIDE: Read through markers and call the function provided by the caller
    ## returns: bool
    def read_through_data(self) -> bool:

        while self.data_manager.continue_reading():
            node = self.data_manager.get_current_node()

            logging.debug(f"{self.data_type}: {node.get_loop_id()}\t\t{str(node.get_start())}")

            # Call the function overriden by the caller
            self.update_file(node)

        return True
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # TO OVERRIDE: Function to update the file
    ## returns: None
    def update_file(self, node) -> None:
        pass
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # TO OVERRIDE: Function to create final file
    ## returns: bool
    def create_final_file(self) -> bool:
        pass
    # ----------------------------------------------------------------------------

# ================================================================================================

SUPPORTED_DATA_TYPES_INIT = {
    "MRK": ProToolsMarkerManager,
    "EDL": ProToolsEDLManager
}

# ================================================================================================