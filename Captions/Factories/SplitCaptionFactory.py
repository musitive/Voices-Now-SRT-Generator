import re

from Captions.TextFormats.ICaption import ICaption
from Captions.TextFormats.SRT import SRT
from Captions.Factories.AbstractCaptionFactory import AbstractCaptionFactory
from Captions.TimeFormats.Nodes.INode import INode

from Projects.SRTProject import SRTProject

from Languages.LanguageSpecificPunctuationPriority import get_priority_regex
from Languages.LanguageDatabase import LanguageDatabase

from Timecodes.Timecode import Timecode

BUFFER_WIDTH = 2

class SplitCaptionFactory(AbstractSplitCaptionFactory):
    def __init__(self, unsplit_caption_factory: AbstractCaptionFactory,
                 sentence_d = '', word_d = ''):
        
        self.unsplit_caption_factory = unsplit_caption_factory

        self.language_database = LanguageDatabase()
        self.project = SRTProject()
        
        self.max_line_len = self.project.language.max_char_count

        self.sentence_d = sentence_d
        self.word_d = word_d

        self.regex = get_priority_regex(self.project.language)


    def create_captions_from_text_and_node(self, text: str, node: INode) -> list[ICaption]:
        return self.__process_text(text, node)


    # Private Methods ---------------------------------------------------------
    def __process_text(self, text: str, node: INode) -> list[ICaption]:
        captions = []

        if self.__should_split(text):
            captions = self.__split_text_and_process(text, node)
        else:
            captions = self.unsplit_caption_factory.create_captions_from_text_and_node(text, node)
        
        return captions
    

    def __should_split(self, text: str) -> bool:
        return len(text) > self.max_line_len


    def __split_text_and_process(self, text: str, node: INode) -> list[ICaption]:
        left, right = self.__split_text(text)

        if not self.__should_split(left) and not self.__should_split(right):
            return self.unsplit_caption_factory.create_captions_from_text_and_node(text, node)
        
        average_frame = self.__find_split_timecode(node, len(text), len(left))

        # TODO: This is bad code
        left_node = node
        left_node.out_time = average_frame
        right_node = node
        right_node.in_time = average_frame

        self.__process_text(left_node, left)
        self.__process_text(right_node, right)


    def __split_text(self, text: str) -> tuple[str, str]:
        split_index = self.__find_split_index(text)

        left = text[:split_index]
        right = text[split_index:]

        return left.strip(), right.strip()


    def __find_split_index(self, text: str) -> int:
        buffered_text = text[BUFFER_WIDTH:-BUFFER_WIDTH]
        for regex in self.regex.split("|"):
            if self.__does_text_contain_punctuation(buffered_text, regex):
                return self.__find_text_best_split_index(buffered_text, regex)


    def __does_text_contain_punctuation(self, text: str, punctuation: str) -> bool:
        return bool(re.search(punctuation, text))


    def __find_text_best_split_index(text: str, regex: str) -> int:
        middle_index = len(text) // 2
        split_index = len(text) + 1 # Initialize to out of bounds

        for m in re.finditer(regex, text):
            if abs(middle_index - m.start()) < abs(middle_index - split_index):
                split_index = m.start()
            else:
                break
            
        if split_index == len(text) + 1:
            raise Exception(f"Split index could not be found:\n{text}")
        
        return split_index+1+BUFFER_WIDTH
        
    
    def __find_split_timecode(self, node: INode, length: int, index: int) -> Timecode:
        in_time = node.get_start_time()
        out_time = node.get_end_time

        # If the split is closer to the beginning, it should have a highter weight
        in_weight = length - index
        out_weight = index

        return self.__weighted_average(in_time, out_time, in_weight, out_weight)
    

    def __weighted_average(self, time_1: Timecode, time_2: Timecode, weight_1: int, weight_2: int) -> Timecode:
        weighted_time_1 = time_1 * weight_1
        weighted_time_2 = time_2 * weight_2
        sum_of_times = weighted_time_1 + weighted_time_2
        weighted_average = sum_of_times // (weight_1 + weight_2)

        return weighted_average