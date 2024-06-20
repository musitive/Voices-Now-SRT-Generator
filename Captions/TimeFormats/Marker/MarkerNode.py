from Captions.TimeFormats.INode import INode

from ProTools.Timecode import Timecode
from ProTools.Marker import Marker

class MarkerNode(INode):
    def __init__(self, marker: Marker):
        self.__start_marker : Marker = marker
        self.__end_marker : Marker = None
        self._next : MarkerNode = None
        self._previous : MarkerNode = None

    def get_loop_id(self) -> str:
        return self.__start_marker.name

    def get_start_time(self) -> Timecode:
        return self.__start_marker.location

    def get_end_time(self) -> Timecode:
        # If there is no end marker, return the next marker
        end = None

        if self.__end_marker != None:
            end = self.__end_marker.location
        elif self._next != None:
            end = self._next.__start_marker.location
        
        return end