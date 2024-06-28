from Projects.SRTProject import SRTProject

from Captions.Factories.AbstractCaptionFactory import AbstractCaptionFactory
from Captions.TextFormats.SRT import SRT
from Captions.TimeFormats.Nodes.INode import INode

class SRTFactory(AbstractCaptionFactory):
    def __init__(self):
        self.current_index = 1

        self.project = SRTProject()
        self.contains_offset = hasattr(self.project, 'srt_offset')

        if self.contains_offset:
            self.offset = self.project.srt_offset


    def create_captions_from_text_and_node(self, text: str, node: INode) -> list[SRT]:
        index = self.current_index
        self.current_index += 1
        start_time = node.get_start_time()
        end_time = node.get_end_time()

        srt = SRT(index, start_time, end_time, text)

        if self.contains_offset:
            srt = srt.create_new_srt_from_offset(self.offset)

        return [srt]