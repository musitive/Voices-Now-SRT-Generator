import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProToolsMarkers")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")

from Captions.FileMaker import FileMaker
from Scripts.ScriptManager import LdsScriptManager
from ProToolsData.ProToolsMarkerManager import ProToolsMarkerManager
from Captions.SRTManager import SRTManager
from Captions.LanguageSpecificSRTManagers import LANG_SRT_MAP

# ================================================================================================

class CaptionMaker(FileMaker):
    # ----------------------------------------------------------------------------
    # Caption Maker
    def __init__(self, timecode_filename: str):
        super().__init__(timecode_filename)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Create captions from the script and timecode markers
    # split:    bool    - split the captions into multiple lines
    def create_captions(self, split: bool = True) -> None:

        # Inner function to update the file
        def update_file(self, marker, next_marker):
            # Get translation from Word Doc
            translation = self.script_manager.get_translation(marker.name)

            # Generate SRT text
            if not self.skip_caption(translation, marker.name):
                self.caption_manager.create_caption(translation.strip(), marker.timecode, next_marker.timecode, split=split)

        # Read through markers
        self.read_through_markers(update_file)

        # Write SRTs to file
        self.caption_manager.write_captions_to_file()
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Logic to skip captions
    # caption:        Caption text
    # marker_name:    Marker name
    def skip_caption(self, caption: str, marker_name) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE"
    # ----------------------------------------------------------------------------

# ================================================================================================

class SRTMaker(CaptionMaker):
    # ----------------------------------------------------------------------------
    # SRT Maker
    # script_filename: str    - the name of the file containing the script data
    # timecode_filename: str  - the name of the file containing the timecode data
    # srt_filename: str       - the name of the file containing the SRT data
    # lang: str               - the language of the SRT data
    def __init__(self, script_filename: str, timecode_filename: str, srt_filename: str, lang: str):
        
        self.script_manager = LdsScriptManager(script_filename)
        if timecode_filename is not None:
            self.marker_manager = ProToolsMarkerManager.from_file(timecode_filename)
        elif self.script_manager.has_timecodes():
            timecode_dict = self.script_manager.get_timecodes()
            self.marker_manager = ProToolsMarkerManager.from_script(timecode_dict)
        else:
            raise Exception("No timecode file provided and no timecodes found in script file")

        if lang in LANG_SRT_MAP:
            self.caption_manager = LANG_SRT_MAP[lang](srt_filename)
        else:
            self.caption_manager = SRTManager(srt_filename, lang=lang)
    # ----------------------------------------------------------------------------

# ================================================================================================