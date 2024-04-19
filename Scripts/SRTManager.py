import re
import thai_segmenter
from functools import reduce
from ProToolsMarkers.Timecode import Timecode
import codecs
import khmernltk
from importlib import reload

import CaptionManager
reload(CaptionManager)

from CaptionManager import CaptionManager

MAX_LINE_LEN = 44              # Maximum number of characters allow in an SRT caption

PRIORITY_BY_LANGUAGE = {
    "ENG": "[\.\!\?\;]|[\,\:\—]|\s",
    "IND": "[\.\!\?\;]|[\,\:\—]|\s",
    "TAH": "[\.\!\?\;]|[\,\:\—]|\s",
}

class SRTManager(CaptionManager):
    """
    SRTManager initializer
    srt_filename: str   - the filename of the SRT file
    max_line_len: int   - the maximum number of characters allowed in an SRT caption
    """
    def __init__(self, srt_filename: str, max_line_len: int = MAX_LINE_LEN, lang: str = "ENG", sentence_d = '', word_d = ''):
        self.srt_id = 1
        self.srt_blocks = []
        self.srt_filename = srt_filename
        self.max_line_len = max_line_len
        self.lang = lang
        self.sentence_d = sentence_d
        self.word_d = word_d


    """
    Inner class to store SRT information
    """
    class SRTInfo:
        def __init__(self, index, start_time, end_time, text):
            self.index = index
            self.start_time = start_time
            self.end_time = end_time
            self.text = text

        def __str__(self):
            start_time = self.start_time.get_timecode_in_ms()
            end_time = self.end_time.get_timecode_in_ms()
            return f"{self.index}\n{start_time} --> {end_time}\n{self.text}\n"


    """
    Create a new caption
    translation: str        - the translated text
    in_time: Timecode       - the time the caption appears on screen
    out_time: Timecode      - the time the caption disappears from the screen
    split: bool             - whether to split the caption into multiple lines
    """
    def create_caption(self, translation: str, in_time: Timecode, out_time: Timecode, split: bool = True):
        if split:
            self.split_caption(in_time, out_time, translation)
        else:
            self.add_srt(in_time, out_time, translation)

        return


    """
    Split the SRT text into blocks of text that are less than the maximum line length
    in_time: Timecode       - the time the caption appears on screen
    out_time: Timecode      - the time the caption disappears from the screen
    text: str               - the text to split
    """
    def split_caption(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        n = len(text)

        if n <= self.max_line_len:
            self.add_srt(in_time, out_time, text.strip())
            return

        left, right = self.split_text_by_language(in_time, out_time, text)
        l = len(left)
        r = len(right)

        if l <= self.max_line_len and r <= self.max_line_len:
            self.add_srt(in_time, out_time, left + "\n" + right)
            return
        
        split_time = self.weighted_average(in_time, out_time, n, l)
        self.split_caption(in_time, split_time, left.strip())
        self.split_caption(split_time, out_time, right.strip())


    """
    Split the text into two parts according to the language
    in_time: Timecode       - the time the caption appears on screen
    out_time: Timecode      - the time the caption disappears from the screen
    text: str               - the text to split
    """
    def split_text_by_language(self, in_time: Timecode, out_time: Timecode, text: str) -> tuple:
        split_index, _ = self.calculate_weighted_split(in_time, out_time, text, False)
        left = text[:split_index]
        right = text[split_index:]

        return left, right


    """
    Split the text into two parts according to the language, with sentence and word tokenizers
    in_time: Timecode       - the time the caption appears on screen
    out_time: Timecode      - the time the caption disappears from the screen
    text: str               - the text to split
    sentence_tokenizer: function    - the sentence tokenizer function
    word_tokenizer: function        - the word tokenizer function
    """
    def split_text_by_token(self, in_time: Timecode, out_time: Timecode, text: str, sentence_tokenizer, word_tokenizer) -> tuple:
        sentences = sentence_tokenizer(text)
        if len(sentences) > 1:
            return self.segmentation_split(in_time, out_time, sentences, self.sentence_d)
        else:
            tokens = word_tokenizer(text)
            return self.segmentation_split(in_time, out_time, tokens, self.word_d)
        

    """
    Split the text into two parts using tokenization, works for both sentence and word tokenization
    in_time: Timecode       - the time the caption appears on screen
    out_time: Timecode      - the time the caption disappears from the screen
    segments: list          - the list of segments to split
    d: str                  - the delimiter to join the segments
    """
    def segmentation_split(self, in_time: Timecode, out_time: Timecode, segments: list, d = '') -> None:
        m = len(segments)
        index = m // 2
        left = reduce(lambda x, y: x + d + y, map(str, segments[:index]))
        right = reduce(lambda x, y: x + d + y, map(str, segments[index:]))
        
        return left, right

    """
    Calculate the weighted split index
    in_time: Timecode    - the time the caption appears on screen
    out_time: Timecode   - the time the caption disappears from the screen
    text: str       - the text to split
    prioritize: bool    - whether to prioritize splitting at punctuation
    """
    def calculate_weighted_split(self, in_time: Timecode, out_time: Timecode, text: str, prioritize: bool = True) -> tuple:
        split_index = self.find_split_index(text, prioritize)
        split_time = self.weighted_average(in_time, out_time, len(text), split_index)
        return split_index, split_time


    """
    Calculate the weighted average of the in_time and out_time
    in_time: Timecode    - the time the caption appears on screen
    out_time: Timecode   - the time the caption disappears from the screen
    n: int          - the total number of characters in the text
    index: int      - the index of the split
    """
    def weighted_average(self, in_time: Timecode, out_time: Timecode, n: int, index: int) -> Timecode:
        in_frame = in_time.get_total_frames()
        out_frame = out_time.get_total_frames()

        average_frame = int((in_frame * (n - index) + out_frame * index) / n)

        return Timecode(average_frame, in_time.frame_rate)

    """
    Find the split index of the text
    text: str       - the text to split
    prioritize: bool    - whether to prioritize splitting at punctuation
    """
    def find_split_index(self, text: str, prioritize: bool = True) -> int:
        def search_text(regex: str, text: str):
            n = len(text) // 2
            split_index = len(text) + 1

            for m in re.finditer(regex, text):
                if abs(n - m.start()) < abs(n - split_index):
                    split_index = m.start()
                else:
                    return split_index+2
                
            return split_index+2

        if prioritize:
            for regex in PRIORITY_BY_LANGUAGE[self.lang].split("|"):
                if bool(re.search(regex, text[1:-1])):
                    return search_text(regex, text[1:-1])
            
        else:
            regex = PRIORITY_BY_LANGUAGE[self.lang]
            return search_text(regex, text[1:-1])
            

    """
    Add a new SRT block to the SRT file
    in_time: Timecode    - the time the caption appears on screen
    out_time: Timecode   - the time the caption disappears from the screen
    text: str       - the caption text
    """
    def add_srt(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        self.srt_blocks.append(self.SRTInfo(self.srt_id, in_time, out_time, text.strip()))
        self.srt_id += 1
    

    """
    Write SRT blocks to the file
    """
    def write_captions_to_file(self):
        srt_file = codecs.open(self.srt_filename, "w+", encoding="utf-8")    # Open SRT file

        for srt in self.srt_blocks:
            srt_file.write(str(srt)+"\n")

        srt_file.close()


class ThaiSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, max_line_len=33, lang="THA", sentence_d=' ')

    """
    Call the split_text_by_language function with the Thai segmenter. This library doesn't seem to be very well optimized.
    https://pypi.org/project/thai-segmenter/
    """
    def split_text_by_language(self, in_time: Timecode, out_time: Timecode, text: str) -> tuple:
        return super().split_text_by_token(in_time, out_time, text, thai_segmenter.sentence_segment, thai_segmenter.tokenize)


class KhmerSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, max_line_len=33, lang="KHM")

    """
    Call the split_text_by_language function with the KhmerNLTK library. This library works great.
    https://pypi.org/project/khmer-nltk/
    """
    def split_text_by_language(self, in_time: Timecode, out_time: Timecode, text: str) -> tuple:
        return super().split_text_by_token(in_time, out_time, text, khmernltk.sentence_tokenize, khmernltk.word_tokenize)