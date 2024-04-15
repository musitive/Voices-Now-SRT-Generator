import Timecode
import re
from importlib import reload
from thai_segmenter import tokenize
from thai_segmenter import sentence_segment
from functools import reduce

reload(Timecode)

from SRTInfo import SRTInfo
from Timecode import Timecode
import codecs

MAX_LINE_LEN = 44              # Maximum number of characters allow in an SRT caption

PRIORITY_BY_LANGUAGE = {
    "ENG": "[\.\!\?\;]|[\,\:\—]|\s",
    "IND": "[\.\!\?\;]|[\,\:\—]|\s",
    "THA": "\s"
}

class SRTManager:
    """
    SRTManager initializer
    srt_filename: str   - the filename of the SRT file
    max_line_len: int   - the maximum number of characters allowed in an SRT caption
    """
    def __init__(self, srt_filename: str, max_line_len: int = MAX_LINE_LEN, lang: str = "ENG"):
        self.srt_id = 1
        self.srt_blocks = []
        self.srt_filename = srt_filename
        self.max_line_len = max_line_len
        self.lang = lang

        if lang == "THA":
            self.max_line_len = 33


    """
    Create SRT blocks from the text
    text: str       - the text to create SRT blocks from  
    in_time: Timecode    - the time the caption appears on screen
    out_time: Timecode   - the time the caption disappears from the screen
    splitSRT: bool  - whether to split the SRT text into blocks
    """
    def create_SRT_blocks(self, text: str, in_time: Timecode, out_time: Timecode):
        if self.lang == "THA":
            self.split_THA_SRT(in_time, out_time, text.strip())
        elif self.lang in PRIORITY_BY_LANGUAGE.keys():
            self.split_SRT(in_time, out_time, text.strip())
        else:
            self.add_srt(in_time, out_time, text.strip())


    def split_THA_SRT(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        n = len(text)

        if n <= self.max_line_len:
            self.add_srt(in_time, out_time, text.strip())
            return

        sentences = sentence_segment(text)
        m = len(sentences)

        if n > self.max_line_len * 2:
            if m > 1:
                self.split_THA_segmenter(in_time, out_time, sentences)
            else:
                tokens = tokenize(text)
                self.split_THA_segmenter(in_time, out_time, tokens)
        elif n > self.max_line_len:
            if m > 1:
                self.split_THA_segmenter(in_time, out_time, sentences)
            else:
                tokens = tokenize(text)
                self.split_THA_segmenter(in_time, out_time, tokens)


    def split_THA_segmenter(self, in_time: Timecode, out_time: Timecode, segments: list, d = '') -> None:
        m = len(segments)
        index = m // 2
        left = reduce(lambda x, y: x + d + y, map(str, segments[:index]))
        right = reduce(lambda x, y: x + d + y, map(str, segments[index:]))
        n = len(left) + len(right)

        if len(left) > self.max_line_len:
            split_time = self.weighted_average(in_time, out_time, n, len(left))
            self.split_THA_SRT(in_time, split_time, left.strip())  # Split the left half of the text
            self.add_srt(split_time, out_time, right.strip())
        elif len(right) > self.max_line_len:
            split_time = self.weighted_average(in_time, out_time, n, len(left))
            self.add_srt(in_time, split_time, left.strip())
            self.split_THA_SRT(split_time, out_time, right.strip())
        else:
            self.add_srt(in_time, out_time, left + "\n" + right)


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
    Split the SRT text into blocks of text that are less than the maximum line length
    text: str    - the text to split
    """
    def split_SRT(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        n = len(text)

        if n <= self.max_line_len:
            self.add_srt(in_time, out_time, text.strip())
            return

        if n > self.max_line_len * 2:
            split_index, split_time = self.calculate_weighted_split(in_time, out_time, text)

            # refactor later to split according to priority
            self.split_SRT(in_time, split_time, text[:split_index].strip())      # Split the left half of the text
            self.split_SRT(split_time, out_time, text[split_index:].strip())     # Split the right half of the text
        elif n > self.max_line_len:
            split_index, split_time = self.calculate_weighted_split(in_time, out_time, text, False)

            if split_index > self.max_line_len:
                self.split_SRT(in_time, split_time, text[:split_index].strip())  # Split the left half of the text
                self.add_srt(split_time, out_time, text[split_index:])
            elif n - split_index - 1 > self.max_line_len:
                self.add_srt(in_time, split_time, text[:split_index])
                self.split_SRT(split_time, out_time, text[split_index:].strip())
            else:
                self.add_srt(in_time, out_time, text[:split_index].strip() + "\n" + text[split_index:].strip())


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
        self.srt_blocks.append(SRTInfo(self.srt_id, in_time, out_time, text.strip()))
        self.srt_id += 1
    

    """
    Write SRT blocks to the file
    """
    def write_SRTs_to_file(self):
        srt_file = codecs.open(self.srt_filename, "w+", encoding="utf-8")    # Open SRT file

        for srt in self.srt_blocks:
            srt_file.write(str(srt)+"\n")

        srt_file.close()