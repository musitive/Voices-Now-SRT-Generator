from ProTools.Marker import Marker
from ProTools.EDL import Clip
from ProTools.Timecode import Timecode

# ================================================================================================
class DataNode:
    # ------------------------------------------------------------------------
    # Linked list node for Pro Tools data
    # data: any    - the data
    def __init__(self, data):
        self.current = data
        self.next = None
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # TO OVERRIDE: Get the current loop
    ## returns: int
    def get_loop_id(self) -> str:
        pass
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # TO OVERRIDE: Get start timecode
    ## returns: Timecode
    def get_start(self) -> Timecode:
        pass
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # TO OVERRIDE: Get end timecode
    ## returns: Timecode
    def get_end(self) -> Timecode:
        pass
    # ------------------------------------------------------------------------

# ================================================================================================

class MarkerNode(DataNode):
    # ------------------------------------------------------------------------
    # Linked list node for markers
    # marker: ProToolsMarker   - the marker data
    # end: ProToolsMarker      - if there is a marker between this and the next marker marking the end of a segment
    # next: MarkerNode         - the next marker in the list
    def __init__(self, marker: Marker):
        self.marker : Marker = marker
        self.end : Marker = None
        self.next : MarkerNode = None
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Get the current loop
    ## returns: str
    def get_loop_id(self) -> str:
        return self.marker.name
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Get start timecode
    ## returns: Timecode
    def get_start(self) -> Timecode:
        return self.marker.location
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Get end timecode
    ## returns: Timecode
    def get_end(self) -> Timecode:
        # If there is no end marker, return the next marker
        if self.end == None and self.next != None:
            return self.next.marker.location
        
        return self.end.location
    # ------------------------------------------------------------------------

# ================================================================================================

class EDLNode(DataNode):
    # ------------------------------------------------------------------------
    # Linked list node for Pro Tools EDL data
    # edl: ProToolsEDL    - the Pro Tools EDL data
    def __init__(self, edl: Clip):
        self.edl : Clip = edl
        self.next : EDLNode = None
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Get the current loop
    ## returns: str
    def get_loop_id(self) -> str:
        return self.edl.loop
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Get start timecode
    ## returns: Timecode
    def get_start(self) -> Timecode:
        return self.edl.start_time
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Get end timecode
    ## returns: Timecode
    def get_end(self) -> Timecode:
        return self.edl.end_time
    # ------------------------------------------------------------------------

# ================================================================================================