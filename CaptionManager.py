import re
import thai_segmenter
from functools import reduce
from Timecode import Timecode
import codecs
import khmernltk

MAX_LINE_LEN = 44              # Maximum number of characters allow in an SRT caption

PRIORITY_BY_LANGUAGE = {
    "ENG": "[\.\!\?\;]|[\,\:\—]|\s",
    "IND": "[\.\!\?\;]|[\,\:\—]|\s",
}

class CaptionManager:
    def __init__(self):
        pass

    def create_caption(self, translation: str, in_time: Timecode, out_time: Timecode):
        pass

    def write_captions_to_file(self):
        pass

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
    Create SRT blocks from the text
    text: str       - the text to create SRT blocks from  
    in_time: Timecode    - the time the caption appears on screen
    out_time: Timecode   - the time the caption disappears from the screen
    splitSRT: bool  - whether to split the SRT text into blocks
    """
    def create_caption(self, text: str, in_time: Timecode, out_time: Timecode):
        self.split_SRT(in_time, out_time, text.strip())


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

        split_index, split_time = self.calculate_weighted_split(in_time, out_time, text, False)
        left = text[:split_index]
        right = text[split_index:]
        l = len(left)
        r = len(right)

        if l <= self.max_line_len and r <= self.max_line_len:
            self.add_srt(in_time, out_time, left + "\n" + right)
            return
        
        split_time = self.weighted_average(in_time, out_time, n, l)
        self.split_SRT(in_time, split_time, left.strip())
        self.split_SRT(split_time, out_time, right.strip())


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


    def special_split(self, in_time: Timecode, out_time: Timecode, text: str, sentence_tokenizer, word_tokenizer) -> None:
        n = len(text)

        if n <= self.max_line_len:
            self.add_srt(in_time, out_time, text.strip())
            return

        sentences = sentence_tokenizer(text)

        if len(sentences) > 1:
            self.segmentation_split(in_time, out_time, sentences, self.sentence_d)
        else:
            tokens = word_tokenizer(text)
            self.segmentation_split(in_time, out_time, tokens, self.word_d)

    def segmentation_split(self, in_time: Timecode, out_time: Timecode, segments: list, d = '') -> None:
        m = len(segments)
        index = m // 2
        left = reduce(lambda x, y: x + d + y, map(str, segments[:index]))
        right = reduce(lambda x, y: x + d + y, map(str, segments[index:]))
        l = len(left)
        r = len(right)
        n = l + r

        if l <= self.max_line_len and r <= self.max_line_len:
            self.add_srt(in_time, out_time, left + "\n" + right)
            return
        
        split_time = self.weighted_average(in_time, out_time, n, l)
        self.split_SRT(in_time, split_time, left.strip())
        self.split_SRT(split_time, out_time, right.strip())


class ThaiSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super(ThaiSRTManager, self).__init__(srt_filename, max_line_len=33, lang="THA", sentence_d=' ')

    def split_SRT(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        self.special_split(in_time, out_time, text, thai_segmenter.sentence_tokenize, thai_segmenter.word_tokenize)


class KhmerSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super(KhmerSRTManager, self).__init__(srt_filename, max_line_len=33, lang="KHM")

    def split_SRT(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        self.special_split(in_time, out_time, text, khmernltk.sentence_tokenize, khmernltk.word_tokenize)