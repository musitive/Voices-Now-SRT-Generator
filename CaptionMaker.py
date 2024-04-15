"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import CaptionManager
from importlib import reload

reload(CaptionManager)

from ProToolsMarkerManager import ProToolsMarkerManager
from ScriptManager import LdsScriptManager
from CaptionManager import SRTManager, ThaiSRTManager, KhmerSRTManager

class CaptionMaker:
    def __init__(self):
        self.markers = None
        self.script_manager = None
        self.caption_manager = None

    """
    Create captions from the script and timecode markers
    """
    def create_captions(self) -> None:
        # Get the first markers
        marker = self.markers.get_next_marker()
        while marker is not None and self.skip_marker(marker.name):
            marker = self.markers.get_next_marker()
        next_marker = self.markers.get_next_marker()
        while next_marker is not None and self.skip_marker(next_marker.name, True):
            next_marker = self.markers.get_next_marker()

        while marker is not None and next_marker is not None:
            # If no more markers, break
            if marker is None or next_marker is None:
                break

            # Get translation from Word Doc
            translation = self.script_manager.get_next_translation().replace("\n", "")

            # Generate SRT text
            if not self.skip_caption(translation, marker.name):
                self.caption_manager.create_caption(translation, marker.timecode, next_marker.timecode, split=True)

            # Update markers
            marker = next_marker
            while marker is not None and self.skip_marker(marker.name):
                marker = self.markers.get_next_marker()
            next_marker = self.markers.get_next_marker()
            while next_marker is not None and self.skip_marker(next_marker.name, True):
                next_marker = self.markers.get_next_marker()

        # Write SRTs to file
        self.caption_manager.write_captions_to_file()

        return


    """
    Logic to skip markers
    name:           Marker name
    is_end:         Is the marker the last marker in the script
    """
    def skip_marker(self, name: str, is_end: bool = False) -> bool:
        if name.isnumeric():
            return False

        if is_end:
            return not (name == 'x' or name == 'END' or name == 'w')
        return name != 'w'
    

    """
    Logic to skip captions
    caption:        Caption text
    marker_name:    Marker name
    """
    def skip_caption(self, caption, marker_name) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE" or marker_name == 'w'


class SRTMaker(CaptionMaker):
    def __init__(self, script_filename: str, timecode_filename: str, srt_filename: str, lang: str):
        self.markers = ProToolsMarkerManager(timecode_filename)              # Open Pro Tools Marker file
        self.script_manager = LdsScriptManager(script_filename)              # Open Word Document

        if lang == "THA":
            self.caption_manager = ThaiSRTManager(srt_filename)
        elif lang == "KHM":
            self.caption_manager = KhmerSRTManager(srt_filename)
        else:
            self.caption_manager = SRTManager(srt_filename, lang=lang)



# Test Case
# if __name__ == '__main__':
#     create_srt_file("tests/BMVL_502_IND.docx", "tests/BMVL_502_timecode.txt", "tests/BMVL_502_IND_refactor.srt")