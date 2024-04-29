from Scripts.SRTManager import SRTManager

import thai_segmenter
import khmernltk
import laonlp
import fugashi

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
    
"""
Japanese SRT Manager
Japanese is a bit more complicated since sometimes it has spaces. It also has three writing systems: Kanji, Hiragana, and Katakana.
In the case that a line is too long, we will use the fugashi library to split the text.
"""
class JapaneseSRTManager(SRTManager):
    def __init__(self, srt_filename: str):
        self.tagger = fugashi.Tagger()
        super().__init__(srt_filename, lang="JPN")


    """
    Call the split_text_by_language function with the fugashi library.
    https://pypi.org/project/fugashi/
    """
    def split_text_by_language(self, text: str) -> tuple:
        try:
            left, right = super().split_text_by_language(text)
        except Exception as e:
            words = self.tagger(text)
            left, right = self.segmentation_split(words)

        return left.strip(), right.strip()
