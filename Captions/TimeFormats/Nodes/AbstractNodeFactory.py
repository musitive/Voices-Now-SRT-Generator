from Captions.TimeFormats.Nodes.INode import INode
from Captions.TimeFormats.Nodes.MarkerNode import MarkerNode
from Captions.TimeFormats.Nodes.EDLNode import EDLNode

from Scripts.Loop import Loop

def initialize_node_factory(data_type: str):
    if data_type == "MRK":
        return MarkerNodeFactory()
    elif data_type == "EDL":
        return EDLNodeFactory()
    elif data_type == "SPT":
        return MarkerNodeFactory()
    else:
        raise ValueError("Invalid data type")

class AbstractNodeFactory:
    def __init__(self):
        pass

    def create_node(self, data) -> INode:
        pass

class MarkerNodeFactory(AbstractNodeFactory):
    def __init__(self):
        super().__init__()

    def create_node(self, data) -> INode:
        node = None

        if type(data) == Loop:
            node = MarkerNode.from_loop(data)
        else:
            node = MarkerNode(data)

        return node
    
class EDLNodeFactory(AbstractNodeFactory):
    def __init__(self):
        super().__init__()

    def create_node(self, data) -> INode:
        return EDLNode(data)