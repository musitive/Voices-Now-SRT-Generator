import re
import codecs
from ProToolsData.Timecode import Timecode
from Captions.LanguageSpecificPunctuationPriority import PRIORITY_BY_LANGUAGE as LANGUAGE, PRIORITY_BY_SCRIPT as SCRIPT_TYPES
from Captions.LanguageManager import LanguageManager

MAX_LINE_LEN = 44              # Maximum number of characters allow in an SRT caption
DEFAULT_SCRIPT_TYPE = "Latin"  # Default script type

# ================================================================================================

class SRTManager:
    # Inner class to store SRT information
    class SRTInfo:
        # ------------------------------------------------------------------------
        # SRT Information
        # index: int         - the index of the SRT block
        # start_time: Timecode   - the start time of the SRT block
        # end_time: Timecode     - the end time of the SRT block
        # text: str          - the text of the SRT block
        def __init__(self, index, start_time, end_time, text):
            self.index = index
            self.start_time = start_time
            self.end_time = end_time
            self.text = text
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # Get the string representation of the SRT block
        def __str__(self):
            start_time = self.start_time.get_timecode_in_ms()
            end_time = self.end_time.get_timecode_in_ms()
            return f"{self.index}\n{start_time} --> {end_time}\n{self.text}\n"
        # ------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # SRTManager initializer
    # srt_filename: str   - the filename of the SRT file
    # max_line_len: int   - the maximum number of characters allowed in an SRT caption
    def __init__(self, srt_filename: str, max_line_len: int = MAX_LINE_LEN,
                 lang_code: str = "ENG", sentence_d = '', word_d = ''):
        self.lang_manager = LanguageManager()

        self.srt_id = 1
        self.srt_blocks = []
        self.srt_filename = srt_filename
        self.max_line_len = max_line_len
        self.lang = lang_code
        self.sentence_d = sentence_d
        self.word_d = word_d

        script_type = self.lang_manager.get_script(lang_code)

        if lang_code in LANGUAGE:
            self.regex = LANGUAGE[lang_code]
        elif script_type in SCRIPT_TYPES:
            self.regex = SCRIPT_TYPES[script_type]
        else:
            self.regex = SCRIPT_TYPES[DEFAULT_SCRIPT_TYPE]
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Create a new caption
    # translation: str        - the translated text
    # in_time: Timecode       - the time the caption appears on screen
    # out_time: Timecode      - the time the caption disappears from the screen
    # split: bool             - whether to split the caption into multiple lines
    ## returns: None
    def create_caption(self, translation: str, in_time: Timecode, out_time: Timecode, split: bool = True) -> None:
        translation = translation.replace("(R)", "")
        # translation = re.sub(r"[\"“”]", "", translation)

        translation = translation.strip()
        if split:
            self.split_caption(in_time, out_time, translation)
        else:
            self.add_srt(in_time, out_time, translation)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Split the SRT text into blocks of text that are less than the maximum line length
    # in_time: Timecode       - the time the caption appears on screen
    # out_time: Timecode      - the time the caption disappears from the screen
    # text: str               - the text to split
    ## returns: None
    def split_caption(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        n = len(text)

        if n <= self.max_line_len:
            self.add_srt(in_time, out_time, text.strip())
            return

        try:
            left, right = self.split_text(text)
        except Exception as e:
            print(f"Error: {e}.")
            self.add_srt(in_time, out_time, text.strip())
            return
        
        l = len(left)
        r = len(right)

        if l <= self.max_line_len and r <= self.max_line_len:
            self.add_srt(in_time, out_time, left.strip() + "\n" + right.strip())
            return
        
        split_time = self.weighted_average(in_time, out_time, n, l)
        self.split_caption(in_time, split_time, left)
        self.split_caption(split_time, out_time, right)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Split the text into two parts according to the language
    # in_time: Timecode       - the time the caption appears on screen
    # out_time: Timecode      - the time the caption disappears from the screen
    # text: str               - the text to split
    def split_text(self, text: str) -> tuple:
        split_index = self.find_split_index(text)
        left = text[:split_index]
        right = text[split_index:]

        return left.strip(), right.strip()
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Calculate the weighted average of the in_time and out_time
    # in_time: Timecode    - the time the caption appears on screen
    # out_time: Timecode   - the time the caption disappears from the screen
    # n: int          - the total number of characters in the text
    # index: int      - the index of the split
    ## returns: Timecode
    def weighted_average(self, in_time: Timecode, out_time: Timecode, n: int, index: int) -> Timecode:
        in_frame = in_time.get_total_frames()
        out_frame = out_time.get_total_frames()
        average_frame = int((in_frame * (n - index) + out_frame * index) / n)

        return Timecode.from_frames(average_frame, in_time.frame_rate)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Find the split index of the text
    # text: str           - the text to split
    # prioritize: bool    - whether to prioritize splitting at punctuation
    ## returns: int       - the index of the split
    def find_split_index(self, text: str, prioritize: bool = True) -> int:
        WIDTH = 2

        def search_text(regex: str, text: str):
            n = len(text) // 2
            split_index = len(text) + 1

            for m in re.finditer(regex, text):
                if abs(n - m.start()) < abs(n - split_index):
                    split_index = m.start()
                else:
                    break
                
            if split_index == len(text) + 1:
                raise Exception(f"Split index could not be found:\n{text}")
            
            return split_index+1+WIDTH

        if prioritize:
            for regex in self.regex.split("|"):
                if bool(re.search(regex, text[WIDTH:-WIDTH])):
                    return search_text(regex, text[WIDTH:-WIDTH])
            
        else:
            return search_text(self.regex, text[WIDTH:-WIDTH])
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Add a new SRT block to the SRT file
    # in_time: Timecode    - the time the caption appears on screen
    # out_time: Timecode   - the time the caption disappears from the screen
    # text: str       - the caption text
    ## returns: None
    def add_srt(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        text = text.strip()
        if text != "":
            self.srt_blocks.append(self.SRTInfo(self.srt_id, in_time, out_time, text))
            self.srt_id += 1
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Write SRT blocks to the file
    # timecode_offset: Timecode    - the timecode offset
    # srtID_offset: int            - the SRT ID offset
    ## returns: int                - the last SRT ID written
    def write_captions_to_file(self, timecode_offset: tuple = None, srtID_offset: int = None) -> int:
        srt_file = codecs.open(self.srt_filename, "w+", encoding="utf-8")    # Open SRT file

        last_srt_index = 0

        for srt in self.srt_blocks:
            if timecode_offset is not None:
                if timecode_offset[0] == "adv":
                    srt.start_time -= timecode_offset[1]
                    srt.end_time -= timecode_offset[1]
                elif timecode_offset[0] == "dly":
                    srt.start_time += timecode_offset[1]
                    srt.end_time += timecode_offset[1]

            if srtID_offset is not None:
                srt.index += srtID_offset

            last_srt_index = srt.index
            
            srt_file.write(str(srt)+"\n")

        srt_file.close()

        return last_srt_index
    # ----------------------------------------------------------------------------
    
# ================================================================================================