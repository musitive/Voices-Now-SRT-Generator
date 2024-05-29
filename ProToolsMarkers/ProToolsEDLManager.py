from ProToolsMarkers.ProToolsEDL import ProToolsEDL, PT_COLUMN_HEADERS
import re

# ================================================================================================

# Indices for Pro Tools EDL data
PT_COLUMN_HEADERS_INDEX = 15
PT_EDL_DATA_START = 16
PT_FRAMERATE_INDEX = 4

# ================================================================================================

class ProToolsEDLManager:
    class EDLNode:
        # ------------------------------------------------------------------------
        # Linked list node for Pro Tools EDL data
        # edl: ProToolsEDL    - the Pro Tools EDL data
        def __init__(self, edl: ProToolsEDL):
            self.edl : ProToolsEDL = edl
            self.next : ProToolsEDLManager.EDLNode = None
        # ------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Pro Tools EDL Manager
    # head_node: EDLNode    - the head node of the linked list
    # frame_rate: float     - the frame rate of the Pro Tools session
    def __init__(self, head_node: EDLNode, frame_rate: float):
        ## Set current node to head node
        self.head_node = head_node
        self.current_node = self.head_node
        self.frame_rate = frame_rate
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Create a ProToolsMarkerManager from a ProTools timecode file
    # filename: str    - the name of the file containing the Pro Tools Marker data
    ## returns: ProToolsMarkerManager
    @staticmethod
    def from_file(filename: str) -> 'ProToolsEDLManager':
        with open(filename, 'r') as timecode_file:
            content = timecode_file.readlines()

            ## Get frame rate
            _, frame_rate = re.split(r"\t", content[PT_FRAMERATE_INDEX])
            frame_rate, _ = re.split("\s", frame_rate, 1)
            frame_rate = float(frame_rate)

            ## Get column headers
            header_data = re.split(r"\t", content[PT_COLUMN_HEADERS_INDEX])
            column_headers = {header_data[i].strip() : i for i in range(len(header_data))}

            ## Check for required fields
            for field in PT_COLUMN_HEADERS_INDEX:
                assert field in column_headers, f"Error: Pro Tools EDL data is missing a required field: {field}"

            ## Create head node for linked list
            line = content[PT_EDL_DATA_START]
            head_node = ProToolsEDLManager.MarkerNode(ProToolsEDL.create_new_EDL(column_headers, line, frame_rate))
            current_node = head_node

            ## Add EDLs to linked list
            for line in content[PT_EDL_DATA_START+1:]:
                next_EDL = ProToolsEDL.create_new_EDL(column_headers, line, frame_rate)

                current_node.next = ProToolsEDLManager.EDLNode(next_EDL)
                current_node = current_node.next
            
            ## Create ProToolsMarkerManager
            return ProToolsEDLManager(head_node, frame_rate)

    # ----------------------------------------------------------------------------
    # Get the current node from the linked list
    ## returns: EDLNode
    def get_current_node(self) -> EDLNode:
        if self.current_node == None:
            return None
        
        node = self.current_node
        self.current_node = self.current_node.next

        return node
    # ----------------------------------------------------------------------------
    
# ================================================================================================