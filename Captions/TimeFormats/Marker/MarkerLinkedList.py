from AbstractLinkedList import AbstractLinkedList
from MarkerNode import MarkerNode
from ProTools.Marker import Marker
from Scripts.Script import Script as Script
from Scripts.Loop import Loop

STARTING_INDEX = 0

NO_TIMECODE_FOUND = "Script does not have timecodes"  

class MarkerLinkedList(AbstractLinkedList):
    # Private -----------------------------------------------------------------
    def __init__(self):
        super().__init__()
    

    # Overrides ---------------------------------------------------------------
    def __create_node(self, data) -> MarkerNode:
        return MarkerNode(data)
    
    
    # Public ------------------------------------------------------------------
    @classmethod
    def from_script(cls, script: Script) -> 'MarkerLinkedList':
        assert script.has_timecodes(), NO_TIMECODE_FOUND

        markers = cls.from_list(MarkerLinkedList.convert_loops_to_markers(script.loops))
        return cls.from_list(markers)
    

    @staticmethod
    def convert_loops_to_markers(loops: list[Loop]) -> list[Marker]:
        markers = []

        for i in len(loops):
            loop = loops[i]
            marker = Marker.from_id_and_loop(i, loop)
            markers.append(marker)

        return markers