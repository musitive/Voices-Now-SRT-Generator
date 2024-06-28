from Timecodes.Timecode import Timecode
from Captions.TextFormats.ICaption import ICaption
from Projects.SRTOffset import SRTOffset, OffsetType

STRING_REPRESENTATION = "{id}\n{start_time} --> {end_time}\n{text}\n\n"

class SRT(ICaption):
    def __init__(self, index: int, start_time: Timecode, end_time: Timecode,
                    text: str):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text


    def __str__(self):
        start_time = self.start_time.convert_to_milliseconds_format()
        end_time = self.end_time.convert_to_milliseconds_format()

        return STRING_REPRESENTATION.format(id=self.index, start_time=start_time,
                                            end_time=end_time, text=self.text)


    def create_new_srt_from_offset(self, offset: SRTOffset) -> 'SRT':
        index = self.index + offset.index_offset

        if offset.time_offset_type == OffsetType.ADVANCE:
            start_time = self.start_time - offset
            end_time = self.end_time - offset
        elif offset.time_offset_type == OffsetType.DELAY:
            start_time = self.start_time + offset
            end_time = self.end_time + offset
        else:
            raise ValueError("Invalid offset type")
        
        return SRT(index, start_time, end_time, self.text)