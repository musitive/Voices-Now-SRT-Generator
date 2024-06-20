"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import sys
import abc

from Captions.TimeFormats.EDL.EDLLinkedList import EDLLinkedList
from Captions.TimeFormats.Marker.MarkerLinkedList import MarkerLinkedList
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

import Captions.TimeFormats
from ProTools.Session import Session
from Scripts.Parser import Parser
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Error Messages
INVALID_DATA_TYPE = "Error: Invalid data type: {0}"
NO_TIMECODE_FILE = "Error: No timecode file provided and no timecodes found in script file"

class AbstractWriter:
    def __init__(self, script_filename: str, timecode_filename: str,
                 final_filename: str, data_type: str = "MRK"):
        
        self.script_parser = Parser()
        self.script = self.script_parser.parse_script(script_filename)

        self.final_filename = final_filename
        self.data_type = data_type

        self.data_manager = self.create_data_manager(data_type)

        
    def create_data_manager(self, data_type: str):
        if data_type == "MRK":
            return Captions.TimeFormats.AbstractLinkedList.MarkerManager.from_file(timecode_filename)


    # TO OVERRIDE: Read through markers and call the function provided by the caller
    ## returns: bool
    def read_through_data(self) -> bool:

        while self.data_manager.should_continue():
            node = self.data_manager.get_current_node()

            logging.debug(f"{self.data_type}: {node.get_loop_id()}\t\t{str(node.get_start())}")

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
