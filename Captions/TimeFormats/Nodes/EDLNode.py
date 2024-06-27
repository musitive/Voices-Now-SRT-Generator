from Captions.TimeFormats.Nodes.INode import INode
from Timecodes.Timecode import Timecode
from ProTools.EDL import EDL

class EDLNode(INode):
    def __init__(self, edl: EDL):
        self.__edl : EDL = edl
        self._next : EDLNode = None
        self._previous : EDLNode = None

    def get_loop_id(self) -> str:
        return self.__edl.loop

    def get_start_time(self) -> Timecode:
        return self.__edl.start_time

    def get_end_time(self) -> Timecode:
        return self.__edl.end_time