from ProTools.Marker import Marker
from ProTools.EDL import EDL
from ProTools.Timecode import Timecode

class DataNode:

    def __init__(self, data):
        self.current = data
        self.next = None

    def get_loop_id(self) -> str:
        pass

    def get_start(self) -> Timecode:
        pass

    def get_end(self) -> Timecode:
        pass


class MarkerNode(DataNode):
    def __init__(self, marker: Marker):
        self.marker : Marker = marker
        self.end : Marker = None
        self.next : MarkerNode = None

    def get_loop_id(self) -> str:
        return self.marker.name

    def get_start(self) -> Timecode:
        return self.marker.location

    def get_end(self) -> Timecode:
        # If there is no end marker, return the next marker
        if self.end == None and self.next != None:
            return self.next.marker.location
        
        return self.end.location


class EDLNode(DataNode):
    def __init__(self, edl: EDL):
        self.edl : EDL = edl
        self.next : EDLNode = None

    def get_loop_id(self) -> str:
        return self.edl.loop

    def get_start(self) -> Timecode:
        return self.edl.start_time

    def get_end(self) -> Timecode:
        return self.edl.end_time
