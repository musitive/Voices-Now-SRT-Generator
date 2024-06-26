import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

from Captions.AbstractWriter import AbstractWriter
from Captions.SRTManager import SRTManager
from Captions.TimeFormats.Nodes import INode
from Languages.LanguageSpecificSRTManagers import LANG_SPECIFIC_SRT_INIT
from ProTools.Timecode import Timecode, OffsetType


class CaptionMaker(AbstractWriter):
    def __init__(self, script_filename: str, timecode_filename: str, data_type: str, lang_code: str,
                 srt_filename: str, max_line_len: int,  split: bool = True):
        super().__init__(script_filename, timecode_filename, srt_filename, data_type)

        self.split = split

        if lang_code in LANG_SPECIFIC_SRT_INIT:
            initializer = LANG_SPECIFIC_SRT_INIT[lang_code]
            if lang_code in ["ZHS", "ZHO", "CMN", "YUE"]:
                self.caption_manager = initializer(srt_filename, max_line_len=max_line_len, lang_code=lang_code)
            else:
                self.caption_manager = initializer(srt_filename, max_line_len=max_line_len)
        else:
            self.caption_manager = SRTManager(srt_filename, lang_code=lang_code)


    def create_captions(self, timecode_offset: Timecode = None, timecode_offset_type = OffsetType, srtID_offset: int = None) -> int:

        # Read through markers
        self.read_through_data()

        # Write SRTs to file
        return self.caption_manager.write_captions_to_file()


    def update_file(self, node: INode) -> None:
            # Get loop ID
            loop = node.get_loop_id()

            # Get translation from Word Doc
            translation = self.script.get_translation(loop)

            # Get timecodes
            start_time = node.get_start_time()
            end_time = node.get_end_time()

            # Generate SRT text
            if not self.skip_caption(translation):
                self.caption_manager.create_caption(translation.strip(), start_time, end_time, self.split)


    def skip_caption(self, caption: str) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE"