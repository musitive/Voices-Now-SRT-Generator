from functools import reduce
from Captions.SRTManager import SRTManager

import thai_segmenter
import khmernltk
import laonlp
import konoha
import botok

### IMPORTANT: If adding a new language specific SRT Manager, make sure to add it to the LANG_SRT_MAP
### dictionary at the bottom of this file.

class LanguageSpecificSRTManager(SRTManager):
    # ----------------------------------------------------------------------------
    # Language specific SRT Manager initializer
    # srt_filename: str       - the filename of the SRT file
    # sentence_tokenizer: function    - the sentence tokenizer function
    # word_tokenizer: function        - the word tokenizer function
    # max_line_len: int       - the maximum number of characters allowed in an SRT caption
    # lang: str               - the language code
    # sentence_d: str         - the delimiter for sentence tokenization
    # word_d: str             - the delimiter for word tokenization
    def __init__(self, srt_filename: str, sentence_tokenizer, word_tokenizer,
                 max_line_len: int = 33, lang: str = "ENG", sentence_d = '', word_d = ''):
        super().__init__(srt_filename, max_line_len, lang, sentence_d, word_d)
        self.sentence_tokenizer = sentence_tokenizer
        self.word_tokenizer = word_tokenizer
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Split the text into two parts according to the language, with sentence and word tokenizers
    # in_time: Timecode       - the time the caption appears on screen
    # out_time: Timecode      - the time the caption disappears from the screen
    # text: str               - the text to split
    # sentence_tokenizer: function    - the sentence tokenizer function
    # word_tokenizer: function        - the word tokenizer function
    ## returns: tuple         - the left and right segments
    def split_text_by_token(self, text: str) -> tuple:
        sentences = self.sentence_tokenizer(text)
        if len(sentences) > 1:
            return self.segmentation_split(sentences, self.sentence_d)
        else:
            tokens = self.word_tokenizer(text)
            return self.segmentation_split(tokens, self.word_d)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Split the text into two parts using tokenization, works for both sentence and word tokenization
    # in_time: Timecode       - the time the caption appears on screen
    # out_time: Timecode      - the time the caption disappears from the screen
    # segments: list          - the list of segments to split
    # d: str                  - the delimiter to join the segments
    ## returns: tuple         - the left and right segments
    def segmentation_split(self, segments: list, d = '') -> tuple:
        m = len(segments)
        index = m // 2
        left = reduce(lambda x, y: x + d + y, map(str, segments[:index]))
        right = reduce(lambda x, y: x + d + y, map(str, segments[index:]))
        
        return left, right
    # ----------------------------------------------------------------------------

# ================================================================================================

# SRT Manager for Thai, using the thai-segmenter library.
# https://pypi.org/project/thai-segmenter/
class ThaiSRTManager(LanguageSpecificSRTManager):
    # ----------------------------------------------------------------------------
    # Thai SRT Manager
    # srt_filename: str       - the filename of the SRT file
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, thai_segmenter.sentence_segment,thai_segmenter.tokenize, max_line_len=33, lang="THA", sentence_d=' ')
    # ----------------------------------------------------------------------------

# ================================================================================================

# SRT Manager for Khmer, using the khmer-nltk library.
# https://pypi.org/project/khmer-nltk/
class KhmerSRTManager(LanguageSpecificSRTManager):
    # ----------------------------------------------------------------------------
    # Khmer SRT Manager
    # srt_filename: str       - the filename of the SRT file
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, khmernltk.sentence_tokenize, khmernltk.word_tokenize, max_line_len=33, lang="KHM")
    # ----------------------------------------------------------------------------

# ================================================================================================

# SRT Manager for Lao, using the laonlp library.
# https://pypi.org/project/laonlp/
class LaoSRTManager(LanguageSpecificSRTManager):
    # ----------------------------------------------------------------------------
    # Lao SRT Manager
    # srt_filename: str       - the filename of the SRT file
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, laonlp.sent_tokenize, laonlp.word_tokenize, max_line_len=33, lang="LAO")
    # ----------------------------------------------------------------------------

# ================================================================================================
    
# Japanese SRT Manager, using the konoha library.
# https://github.com/himkt/konoha
class JapaneseSRTManager(LanguageSpecificSRTManager):
    # ----------------------------------------------------------------------------
    # Japanese SRT Manager
    # srt_filename: str       - the filename of the SRT file
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, self.sentence_tokenize, self.word_tokenize, max_line_len=33, lang="JPN")
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Wrapper function for the sentence tokenizer in the botok library.
    # text: str               - the text to tokenize
    ## returns: list          - the list of tokens
    def sentence_tokenize(self, text: str) -> list:
        t = konoha.SentenceTokenizer()
        return t.tokenize(text)
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Wrapper function for the word tokenizer in the botok library.
    # text: str               - the text to tokenize
    ## returns: list          - the list of tokens
    def word_tokenize(self, text: str) -> list:
        t = konoha.WordTokenizer()
        return t.tokenize(text)
    # ----------------------------------------------------------------------------

# ================================================================================================

# SRT Manager for Tibetan, using the botok library.
# https://pypi.org/project/botok/
class TibetanSRTManager(LanguageSpecificSRTManager):
    # ----------------------------------------------------------------------------
    # Tibetan SRT Manager
    # srt_filename: str       - the filename of the SRT file
    def __init__(self, srt_filename: str):
        super().__init__(srt_filename, self.sentence_tokenize, self.word_tokenize, max_line_len=33, lang="TIB")
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Wrapper function for the sentence tokenizer in the botok library.
    # text: str               - the text to tokenize
    ## returns: list          - the list of tokens
    def sentence_tokenize(self, text: str) -> list:
        t = botok.Text(text)
        return t.tokenize_sentences_plaintext()
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Wrapper function for the word tokenizer in the botok library.
    # text: str               - the text to tokenize
    ## returns: list          - the list of tokens
    def word_tokenize(self, text: str) -> list:
        t = botok.Text(text)
        return t.tokenize_words_raw_text()
    # ----------------------------------------------------------------------------
    
# ================================================================================================

# Map language codes to SRT Managers
LANG_SRT_MAP = {
    "THA": ThaiSRTManager,
    "KHM": KhmerSRTManager,
    "LAO": LaoSRTManager,
    "JPN": JapaneseSRTManager,
    "TIB": TibetanSRTManager
}

# ================================================================================================