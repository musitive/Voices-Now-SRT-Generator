from Timecodes.Timecode import Timecode

STRING_REPRESENTATION = "{id}\n{start_time} --> {end_time}\n{text}\n\n"

class SRT:
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
