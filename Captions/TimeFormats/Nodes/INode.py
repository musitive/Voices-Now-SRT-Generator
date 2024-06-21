from ProTools.Timecode import Timecode

class INode:
    def get_loop_id(self) -> str:
        pass

    def get_start_time(self) -> Timecode:
        pass

    def get_end_time(self) -> Timecode:
        pass