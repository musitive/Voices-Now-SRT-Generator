from Captions.TimeFormats.ProToolsLinkedList import DataNode, EDLNode
from ProTools.EDL import EDL

STARTING_INDEX = 0

class LinkedList:
    def __init__(self, head_node: DataNode):
        self.head_node = head_node
        self.current_node = self.head_node


    def should_continue(self) -> bool:
        return self.current_node != None


    def get_current_node(self) -> DataNode:
        if self.current_node == None:
            return None
        
        node = self.current_node
        self.current_node = self.current_node.next

        return node


    @classmethod
    def from_edls(cls, edls: list[EDL]) -> 'LinkedList':
        head_node = EDLNode(edls[STARTING_INDEX])
        current_node = head_node

        for edl in edls[STARTING_INDEX+1:]:
            current_node.next = EDLNode(edl)
            current_node = current_node.next

        return cls(head_node)