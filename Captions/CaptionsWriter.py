import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

from Captions.AbstractWriter import AbstractWriter
from Languages.LanguageSpecificSRTManagers import initialize_caption_manager
from Captions.TimeFormats.Nodes import INode
from ProTools.Timecode import Timecode, OffsetType


class CaptionMaker(AbstractWriter):
    def __init__(self, script_filename: str, timecode_filename: str,
                 data_type: str, lang_code: str, srt_filename: str,
                 max_line_len: int, split: bool = True,
                 timecode_offset: Timecode = None,
                 timecode_offset_type: OffsetType = None, srt_offset: int = None):
        
        super().__init__(script_filename, timecode_filename, srt_filename, data_type)

        self.split = split
        self.caption_manager = initialize_caption_manager(srt_filename, lang_code, max_line_len,
                                                          timecode_offset, timecode_offset_type, srt_offset)



    def create_captions(self) -> int:
        self.read_through_data()
        self.caption_manager.write_captions_to_file()
        return self.caption_manager.current_srt_id


    def update_file(self, node: INode) -> None:
            # Get loop ID
            loop_id = node.get_loop_id()

            # Get translation from Word Doc
            translation = self.script.get_translation(loop_id)

            # Get timecodes
            start_time = node.get_start_time()
            end_time = node.get_end_time()

            # Generate SRT text
            if not self.skip_caption(translation):
                self.caption_manager.create_caption(translation.strip(), start_time, end_time, self.split)


    def skip_caption(self, caption: str) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE"