from Timecodes.Timecode import Timecode, OffsetType

class SRTOffset:
    def __init__(self, time_offset: Timecode = None, time_offset_type: OffsetType = None,
                 index_offset: int = None):
        
        self.time_offset = time_offset
        self.time_offset_type = time_offset_type
        self.index_offset = index_offset