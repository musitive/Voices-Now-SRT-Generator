from AbstractLinkedList import AbstractLinkedList
from Captions.TimeFormats.EDLNode import EDLNode
from ProTools.EDL import EDL

STARTING_INDEX = 0

class EDLLinkedList(AbstractLinkedList):
    # Private -----------------------------------------------------------------
    def __init__(self):
        super().__init__()
    

    # Overrides ---------------------------------------------------------------
    def __create_node(self, data) -> EDLNode:
        return EDLNode(data)