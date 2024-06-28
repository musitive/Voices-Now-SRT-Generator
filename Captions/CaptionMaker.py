import sys
import logging
import codecs

sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/ProTools")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Scripts")
sys.path.append("~/Documents/GitHub/Voices-Now-SRT-Generator/Captions")

from Captions.__init__ import initialize_caption_factory
from Captions.TimeFormats.Nodes.INode import INode
from Captions.TimeFormats.LinkedList import LinkedList
from Captions.TextFormats.ICaption import ICaption

from Projects.SRTProject import SRTProject


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Error Messages
NO_TIMECODE_FILE = "Error: No timecode file provided and no timecodes found in script file"

# Constants
SKIPPABLE_CAPTIONS = ["(R)", "DO NOT TRANSLATE"]


class CaptionMaker:
    def __init__(self, split: bool = True):
        self.project = SRTProject()
        self.linkedlist = LinkedList(self.project.data_type)
        self.caption_factory = initialize_caption_factory(split=split)
        self.captions: list[ICaption] = []


    # Public Methods ----------------------------------------------------------
    def create_captions(self) -> None:
        self.__create_captions_from_linkedlist()
        self.__write_captions_to_file()


    # Private Methods ---------------------------------------------------------
    def __write_captions_to_file(self) -> None:
        with codecs.open(self.srt_filename, "w+", encoding="utf-8") as srt_file:
            for srt in self.srt_blocks:
                srt_file.write(str(srt))


    def __create_captions_from_linkedlist(self) -> None:
        while self.linkedlist.should_continue():
            node = self.linkedlist.iterate_current_node()
            self.__add_captions_from_node(node)
    

    def __add_captions_from_node(self, node: INode) -> None:
        self.__log_node(node)

        loop_id = node.get_loop_id()
        translation = self.project.script.get_translation(loop_id)

        if not self.__should_skip_caption(translation):
            captions = self.caption_factory.create_captions_from_text_and_node(translation, node)
            self.captions.append(captions)


    def __should_skip_caption(self, caption: str) -> bool:
        return caption in SKIPPABLE_CAPTIONS
    

    def __log_node(self, node: INode) -> None:
        data_type = self.project.data_type
        loop_id = node.get_loop_id()
        start_time = node.get_start_time()

        logging.debug(f"{data_type}: {loop_id}\t\t{str(start_time)}")