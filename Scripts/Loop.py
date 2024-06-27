from Timecodes.Timecode import Timecode

class Loop:
    def __init__(self, id: str, character: str, english: str, translation: str,
                 start_time: Timecode = None, end_time: Timecode = None):
        self.id = id
        self.character = character
        self.english = english
        self.translation = translation
        self.start_time = start_time
        self.end_time = end_time