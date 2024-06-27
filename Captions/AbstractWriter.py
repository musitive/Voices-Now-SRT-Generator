"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import sys
import abc

sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

from Captions.TimeFormats.LinkedList import LinkedList
from Projects.SRTProject import SRTProject
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Error Messages
INVALID_DATA_TYPE = "Error: Invalid data type: {0}"
NO_TIMECODE_FILE = "Error: No timecode file provided and no timecodes found in script file"

class AbstractWriter:
    def __init__(self):
        self.project = SRTProject()
        self.data_manager = self.create_data_manager(self.project.data_type)

        
    def create_data_manager(self, data_type: str):
        data_manager = LinkedList(data_type)

        if data_type == "SPT":
            data_manager.append_list_to_end(self.project.script.loops)
        elif data_type == "MRK":
            data_manager.append_list_to_end(self.project.session.markers)
        elif data_type == "EDL":
            data_manager.append_list_to_end(self.project.session.tracks[0].channels[0])

        return data_manager


    # TO OVERRIDE: Read through markers and call the function provided by the caller
    ## returns: bool
    def read_through_data(self) -> bool:

        while self.data_manager.should_continue():
            node = self.data_manager.iterate_current_node()

            logging.debug(f"{self.project.data_type}: {node.get_loop_id()}\t\t{str(node.get_start_time())}")

            # Call the function overriden by the caller
            self.update_file(node)

        return True

    # TO OVERRIDE: Function to update the file
    @abc.abstractmethod
    def update_file(self, node) -> None:
        pass

    # TO OVERRIDE: Function to create final file
    @abc.abstractmethod
    def create_final_file(self) -> bool:
        pass
