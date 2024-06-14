from ProToolsDataManager import ProToolsDataManager
from Marker import Marker
from ProToolsLinkedList import MarkerNode
from Session import Session
import re

END_MARKER_NAMES = ['x', 'END']
SKIP_MARKER_NAMES = ['w']

class ProToolsMarkerManager(ProToolsDataManager):
    def __init__(self, head_node: MarkerNode, frame_rate: float):
        """Constructor for the ProToolsMarkerManager class
        
        Keyword arguments:
        head_node: MarkerNode -- the head node of the linked list of markers
        frame_rate: float -- the frame rate of the markers
        """
        super().__init__(head_node, frame_rate)

    @classmethod
    def from_file(cls, filename: str):
        """Constructor for the ProToolsMarkerManager class using a text file
        
        Keyword arguments:
        filename: str -- the name of the file containing the Pro Tools Marker data
        """

        session = Session.from_file(filename)

        head_node = MarkerNode(session.markers[0])
        current_node = head_node

        for marker in session.markers[1:]:
            if marker.name in END_MARKER_NAMES and current_node.end == None:
                current_node.end = marker
            elif marker.name in SKIP_MARKER_NAMES:
                continue
            else:
                current_node.next = MarkerNode(marker)
                current_node = current_node.next
            
        return cls(head_node, session.frame_rate)
        

    # ----------------------------------------------------------------------------
    # Create a ProToolsMarkerManager from a dictionary of timecodes
    # timecodes: dict    - the dictionary of timecodes
    ## returns: ProToolsMarkerManager
    @classmethod
    def from_script(cls, timecodes: dict):
        make_node = lambda key: MarkerNode(Marker(key, timecodes[key], None, None, key, 24.0))
        time_iter = iter(timecodes)
        key = next(time_iter)
        head_node = make_node(key)
        current_node = head_node

        for key in time_iter:
            next_node = make_node(key)
            current_node.next = next_node
            current_node = next_node
        
        current_node.next = MarkerNode(Marker(len(timecodes.keys()), str(current_node.marker.location + 1), None, None, "END", 24.0))

        return cls(head_node, 24.0)
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Continue reading the data
    ## returns: bool
    def continue_reading(self) -> bool:
        # if self.current_node == None:
        #     return False
            
        # marker = self.current_node.marker
        # next_node = self.current_node.next

        # # If no more markers, break
        # if marker == None or next_node == None or next_node.marker == None:
        #     return False

        return self.current_node != None
    # ----------------------------------------------------------------------------