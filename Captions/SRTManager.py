import re
import codecs
from Timecodes.Timecode import Timecode, OffsetType
from Languages.LanguageSpecificPunctuationPriority import PRIORITY_BY_LANGUAGE as LANGUAGE, PRIORITY_BY_SCRIPT as SCRIPT_TYPES
from Languages.LanguageDatabase import LanguageDatabase
from Captions.TextFormats.SRT import SRT
from Projects.SRTProject import SRTProject

MAX_LINE_LEN = 44              # Maximum number of characters allow in an SRT caption
DEFAULT_SCRIPT_TYPE = "Latin"  # Default script type



class SRTManager:
    def __init__(self, sentence_d = '', word_d = ''):
        self.lang_manager = LanguageDatabase()

        self.project = SRTProject()

        self.current_srt_id = srtID_offset
        self.srt_blocks = []
        self.sentence_d = sentence_d
        self.word_d = word_d

        self.initialize_regex(self.project.language)


    def create_caption(self, translation: str, in_time: Timecode, out_time: Timecode, split: bool = True) -> None:
        translation = translation.replace("(R)", "")
        # translation = re.sub(r"[\"“”]", "", translation)

        translation = translation.strip()
        if split:
            self.split_caption(in_time, out_time, translation)
        else:
            self.add_srt(in_time, out_time, translation)


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


    def split_text(self, text: str) -> tuple:
        split_index = self.find_split_index(text)
        left = text[:split_index]
        right = text[split_index:]

        return left.strip(), right.strip()


    def weighted_average(self, in_time: Timecode, out_time: Timecode, n: int, index: int) -> Timecode:
        in_frame = in_time.get_total_frames()
        out_frame = out_time.get_total_frames()
        average_frame = int((in_frame * (n - index) + out_frame * index) / n)

        return Timecode.from_total_frames(average_frame, in_time.frame_rate)


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


    def add_srt(self, in_time: Timecode, out_time: Timecode, text: str) -> None:
        text = text.strip()
        if text != "":
            in_time = self.offset_timecode(in_time)
            out_time = self.offset_timecode(out_time)
            srt = SRT(self.current_srt_id, in_time, out_time, text)
            self.srt_blocks.append(srt)
            self.current_srt_id += 1


    def write_captions_to_file(self) -> None:
        with codecs.open(self.srt_filename, "w+", encoding="utf-8") as srt_file:
            for srt in self.srt_blocks:
                srt_file.write(str(srt))


    def offset_timecode(self, timecode: Timecode) -> Timecode:
        if self.timecode_offset is None:
            return timecode
        elif self.timecode_offset_type == OffsetType.ADVANCE:
            return timecode - self.timecode_offset
        elif self.timecode_offset_type == OffsetType.DELAY:
            return timecode + self.timecode_offset


    def initialize_regex(self, language_code: str):
        script_type = self.lang_manager.get_script_type(language_code)

        if language_code in LANGUAGE:
            self.regex = LANGUAGE[language_code]
        elif script_type in SCRIPT_TYPES:
            self.regex = SCRIPT_TYPES[script_type]
        else:
            self.regex = SCRIPT_TYPES[DEFAULT_SCRIPT_TYPE]