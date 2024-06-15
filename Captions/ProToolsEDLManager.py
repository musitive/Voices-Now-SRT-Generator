from Captions.ProToolsDataManager import ProToolsDataManager
from ProTools.EDL import EDL, ColumnHeaders
from ProTools.Session import Session
from Captions.ProToolsLinkedList import EDLNode
import re

# ================================================================================================

# Indices for Pro Tools EDL data
PT_COLUMN_HEADERS_INDEX = 15
PT_EDL_DATA_START = 16
PT_FRAMERATE_INDEX = 4

# ================================================================================================

class ProToolsEDLManager(ProToolsDataManager):
    # ----------------------------------------------------------------------------
    # Pro Tools EDL Manager
    # head_node: EDLNode    - the head node of the linked list
    # frame_rate: float     - the frame rate of the Pro Tools session
    def __init__(self, head_node: EDLNode, frame_rate: float):
        
        super().__init__(head_node, frame_rate)
    # ----------------------------------------------------------------------------

    @classmethod
    def from_file(cls, filename: str):
        """Constructor for the ProToolsMarkerManager class using a text file
        
        Keyword arguments:
        filename: str -- the name of the file containing the Pro Tools Marker data
        """

        session = Session.from_file(filename)

        # TODO: Fix logic for EDL data

        caption_track = session.tracks[0]
        caption_channel = caption_track.channels[0]
        first_edl = caption_channel[0]

        head_node = EDLNode(first_edl)
        current_node = head_node

        for edl in caption_channel[1:]:
            current_node.next = EDLNode(edl)
            current_node = current_node.next

        return cls(head_node, session.frame_rate)