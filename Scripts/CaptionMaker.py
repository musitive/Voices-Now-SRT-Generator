import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProToolsMarkers")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")

from Scripts.FileMaker import FileMaker
from Scripts.ScriptManager import LdsScriptManager
from ProToolsMarkers.ProToolsMarkerManager import ProToolsMarkerManager
from Scripts.SRTManager import SRTManager
import Scripts.LanguageSpecificSRTManagers as LSSM

LANG_SRT_MAP = {
    "THA": LSSM.ThaiSRTManager,
    "KHM": LSSM.KhmerSRTManager,
    "LAO": LSSM.LaoSRTManager
}

class CaptionMaker(FileMaker):
    def __init__(self, timecode_filename: str):
        super().__init__(timecode_filename)


    """
    Create captions from the script and timecode markers
    """
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

        return


    """
    Logic to skip captions
    caption:        Caption text
    marker_name:    Marker name
    """
    def skip_caption(self, caption: str, marker_name) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE" or marker_name == 'w'


class SRTMaker(CaptionMaker):
    def __init__(self, script_filename: str, timecode_filename: str, srt_filename: str, lang: str):
        self.marker_manager = ProToolsMarkerManager(timecode_filename)          # Open Pro Tools Marker file
        self.script_manager = LdsScriptManager(script_filename)                 # Open Word Document

        if lang in LANG_SRT_MAP:
            self.caption_manager = LANG_SRT_MAP[lang](srt_filename)
        else:
            self.caption_manager = SRTManager(srt_filename, lang=lang)


# Test Case
# if __name__ == '__main__':
#     create_srt_file("tests/BMVL_502_IND.docx", "tests/BMVL_502_timecode.txt", "tests/BMVL_502_IND_refactor.srt")