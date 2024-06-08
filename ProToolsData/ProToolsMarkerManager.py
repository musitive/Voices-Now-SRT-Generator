from ProToolsData.ProToolsDataManager import ProToolsDataManager
from ProToolsData.ProToolsMarker import ProToolsMarker, PT_COLUMN_HEADERS
from ProToolsData.ProToolsLinkedList import MarkerNode
import re

# ================================================================================================

# Indices for Pro Tools Marker data
PT_COLUMN_HEADERS_INDEX = 11
PT_MARKER_DATA_START = 12
PT_FRAMERATE_INDEX = 4

# ================================================================================================

class ProToolsMarkerManager(ProToolsDataManager):
    # ----------------------------------------------------------------------------
    # Pro Tools Marker Manager
    # filename: str    - the name of the file containing the Pro Tools Marker data
    def __init__(self, head_node: MarkerNode, frame_rate: float):
        super().__init__(head_node, frame_rate)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Create a ProToolsMarkerManager from a ProTools timecode file
    # filename: str    - the name of the file containing the Pro Tools Marker data
    ## returns: ProToolsMarkerManager
    @staticmethod
    def from_file(filename: str) -> 'ProToolsMarkerManager':
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
            for field in PT_COLUMN_HEADERS:
                assert field in column_headers, f"Error: Pro Tools Marker data is missing a required field: {field}"

            ## Create head node for linked list
            line = content[PT_MARKER_DATA_START]
            head_node = MarkerNode(ProToolsMarker.create_new_marker(column_headers, line, frame_rate))
            current_node = head_node

            ## Add markers to linked list
            for line in content[PT_MARKER_DATA_START+1:]:
                if line.strip() == "":
                    continue

                next_marker = ProToolsMarker.create_new_marker(column_headers, line, frame_rate)

                # If the next marker is the end of a segment, set the current node's end to the next marker
                # Otherwise, add the next marker to the linked list
                if next_marker.loop_id in ['x', 'END'] or \
                   (next_marker.loop_id == 'w' and current_node.end == None):

                    current_node.end = next_marker
                else:
                    current_node.next = MarkerNode(next_marker)
                    current_node = current_node.next
            
            ## Create ProToolsMarkerManager
            return ProToolsMarkerManager(head_node, frame_rate)
        

    # ----------------------------------------------------------------------------
    # Create a ProToolsMarkerManager from a dictionary of timecodes
    # timecodes: dict    - the dictionary of timecodes
    ## returns: ProToolsMarkerManager
    @staticmethod
    def from_script(timecodes: dict) -> 'ProToolsMarkerManager':
        make_node = lambda key: MarkerNode(ProToolsMarker(key, timecodes[key], None, None, key, 24.0))
        time_iter = iter(timecodes)
        key = next(time_iter)
        head_node = make_node(key)
        current_node = head_node

        for key in time_iter:
            next_node = make_node(key)
            current_node.next = next_node
            current_node = next_node
        
        current_node.next = MarkerNode(ProToolsMarker(len(timecodes.keys()), str(current_node.marker.timecode + 1), None, None, "END", 24.0))

        return ProToolsMarkerManager(head_node, 24.0)
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Continue reading the data
    ## returns: bool
    def continue_reading(self) -> bool:
        if self.current_node == None:
            return False
            
        marker = self.current_node.marker
        next_node = self.current_node.next

        # If no more markers, break
        if marker == None or next_node == None or next_node.marker == None:
            return False

        return self.current_node != None
    # ----------------------------------------------------------------------------
    
# ================================================================================================