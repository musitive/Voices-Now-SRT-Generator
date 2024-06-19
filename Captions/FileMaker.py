"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

from Captions.TimeFormats.ProToolsMarkerManager import ProToolsMarkerManager
from Captions.TimeFormats.LinkedList import LinkedList
from Scripts.Script import Script
from ProTools.Session import Session
from Scripts.Parser import Parser
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Error Messages
INVALID_DATA_TYPE = "Error: Invalid data type: {0}"
NO_TIMECODE_FILE = "Error: No timecode file provided and no timecodes found in script file"

class FileMaker:
    def __init__(self, script_filename: str, timecode_filename: str,
                 final_filename: str, data_type: str = "MRK"):
        
        self.script_parser = Parser()
        self.script = self.script_parser.parse_script(script_filename)

        self.final_filename = final_filename
        self.data_type = data_type

        self.generate_timecodes(timecode_filename)

        
    def generate_timecodes(self, filename: str) -> None:
        if filename is not None:
            self.generate_timecodes_from_file(filename)
        elif self.script.has_timecodes():
            self.generate_timecodes_from_script()
        else:
            raise Exception(NO_TIMECODE_FILE)
        
        
    def generate_timecodes_from_file(self, filename: str) -> None:
        session = Session.from_file(filename)

        caption_track = session.tracks[0]
        caption_channel = caption_track.channels[0]
        assert data_type in SUPPORTED_DATA_TYPES_INIT, INVALID_DATA_TYPE.format(self.data_type)

        initializer = SUPPORTED_DATA_TYPES_INIT[data_type]
        self.data_manager = initializer.from_file(filename)


    def generate_timecodes_from_script(self) -> None:
        timecode_dict = self.script_parser.get_timecodes()
        self.data_manager = ProToolsMarkerManager.from_script(timecode_dict)


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
    ## returns: None
    def update_file(self, node) -> None:
        pass

    # TO OVERRIDE: Function to create final file
    ## returns: bool
    def create_final_file(self) -> bool:
        pass
