from Captions.ProToolsLinkedList import DataNode

# ================================================================================================

class ProToolsDataManager:
    # ----------------------------------------------------------------------------
    # Pro Tools Data Manager
    # head_node: DataNode   - the head node of the linked list
    # frame_rate: float     - the frame rate of the Pro Tools session
    def __init__(self, head_node: DataNode, frame_rate: float):
        ## Set current node to head node
        self.head_node = head_node
        self.current_node = self.head_node
        self.frame_rate = frame_rate
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Create a ProToolsDataManager from a ProTools timecode file
    # filename: str    - the name of the file containing the Pro Tools Marker data
    # data_type: str   - the type of data to create
    ## returns: ProToolsDataManager
    @staticmethod
    def from_file(filename: str) -> 'ProToolsDataManager':
        pass
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Continue reading the data
    ## returns: bool
    def continue_reading(self) -> bool:
        return self.current_node != None
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Get the current node
    ## returns: DataNode
    def get_current_node(self) -> DataNode:
        if self.current_node == None:
            return None
        
        node = self.current_node
        self.current_node = self.current_node.next

        return node
    # ----------------------------------------------------------------------------

# ================================================================================================