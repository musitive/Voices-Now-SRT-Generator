import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProToolsMarkers")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")

from Captions.FileMaker import FileMaker
from Captions.SRTManager import SRTManager
from ProToolsData.ProToolsLinkedList import DataNode
from Captions.LanguageSpecificSRTManagers import LANG_SPECIFIC_SRT_INIT
from ProToolsData.Timecode import Timecode

# ================================================================================================

class CaptionMaker(FileMaker):
    # ----------------------------------------------------------------------------
    # Caption Maker
    # script_filename:    str     - the name of the script file
    # timecode_filename:  str     - the name of the timecode file
    # data_type:          str     - the type of data
    # lang:               str     - the language of the captions
    # srt_filename:       str     - the name of the SRT file
    # split:              bool    - split the captions into multiple lines
    def __init__(self, script_filename: str, timecode_filename: str, data_type: str, lang_code: str, srt_filename: str,  split: bool = True):
        super().__init__(script_filename, timecode_filename, srt_filename, data_type)

        self.split = split

        if lang_code in LANG_SPECIFIC_SRT_INIT:
            initializer = LANG_SPECIFIC_SRT_INIT[lang_code]
            self.caption_manager = initializer(srt_filename)
        else:
            self.caption_manager = SRTManager(srt_filename, lang_code=lang_code)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Create captions from the script and timecode markers
    # split:    bool                - split the captions into multiple lines
    # timecode_offset: Timecode     - the timecode offset
    # srtID_offset: int             - the SRT ID offset
    ## returns: int                 - the number of captions created
    def create_captions(self, timecode_offset: tuple = None, srtID_offset: int = None) -> int:

        # Read through markers
        self.read_through_data()

        # Write SRTs to file
        return self.caption_manager.write_captions_to_file(timecode_offset, srtID_offset)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Function to update the file
    def update_file(self, node: DataNode) -> None:
            # Get loop ID
            loop = node.get_loop_id()

            # Get translation from Word Doc
            translation = self.script_manager.get_translation(loop)

            # Get timecodes
            start_time = node.get_start()
            end_time = node.get_end()

            # Generate SRT text
            if not self.skip_caption(translation):
                self.caption_manager.create_caption(translation.strip(), start_time, end_time, self.split)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Logic to skip captions
    # caption:        Caption text
    # marker_name:    Marker name
    def skip_caption(self, caption: str) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE"
    # ----------------------------------------------------------------------------

# ================================================================================================