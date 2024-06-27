import sys
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

from Captions.AbstractWriter import AbstractWriter
from Languages.LanguageSpecificSRTManagers import initialize_caption_manager
from Captions.TimeFormats.Nodes import INode

class CaptionMaker(AbstractWriter):
    def __init__(self, split: bool = True):
        
        super().__init__()

        self.split = split
        self.caption_manager = initialize_caption_manager()


    def create_captions(self) -> int:
        self.read_through_data()
        self.caption_manager.write_captions_to_file()
        return self.caption_manager.current_srt_id


    def update_file(self, node: INode) -> None:
            # Get loop ID
            loop_id = node.get_loop_id()

            # Get translation from Word Doc
            translation = self.project.script.get_translation(loop_id)

            # Get timecodes
            start_time = node.get_start_time()
            end_time = node.get_end_time()

            # Generate SRT text
            if not self.skip_caption(translation):
                self.caption_manager.create_caption(translation.strip(), start_time, end_time, self.split)


    def skip_caption(self, caption: str) -> bool:
        return caption == "(R)" or caption == "DO NOT TRANSLATE"