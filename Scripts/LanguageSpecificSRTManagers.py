from Scripts.SRTManager import SRTManager
from ProToolsMarkers.Timecode import Timecode

import thai_segmenter
import khmernltk
import laonlp

class ThaiSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, max_line_len=33, lang="THA", sentence_d=' ')


    """
    Call the split_text_by_language function with the Thai segmenter. This library doesn't seem to be very well optimized.
    https://pypi.org/project/thai-segmenter/
    """
    def split_text_by_language(self, text: str) -> tuple:
        return super().split_text_by_token(text, thai_segmenter.sentence_segment, thai_segmenter.tokenize)


class KhmerSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, max_line_len=33, lang="KHM")


    """
    Call the split_text_by_language function with the KhmerNLTK library. This library works great.
    https://pypi.org/project/khmer-nltk/
    """
    def split_text_by_language(self, text: str) -> tuple:
        return super().split_text_by_token(text, khmernltk.sentence_tokenize, khmernltk.word_tokenize)
    

class LaoSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, max_line_len=33, lang="LAO")


    """
    Call the split_text_by_language function with the KhmerNLTK library. This library works great.
    https://pypi.org/project/khmer-nltk/
    """
    def split_text_by_language(self, text: str) -> tuple:
        return super().split_text_by_token(text, laonlp.sent_tokenize, laonlp.word_tokenize)