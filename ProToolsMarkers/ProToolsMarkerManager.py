"""
Code to extract Pro Tools Markers
Author: Dallin Frank

Run test cases:
py -m unittest TestProToolsMarkerManager
"""

from ProToolsMarkers.ProToolsMarker import ProToolsMarker, PT_MARKER_ID, PT_LOCATION_ID, PT_TIMEREF_ID, PT_UNITS_ID, PT_NAME_ID, PT_COMMENTS_ID
import re

# ================================================================================================

# --------------------------------------------------------------------------------
# Indices for Pro Tools Marker data
PT_COLUMN_HEADERS = 11
PT_MARKER_DATA_START = 12
PT_FRAMERATE_INDEX = 4
# --------------------------------------------------------------------------------

# ================================================================================================

class ProToolsMarkerManager:
    class MarkerNode:
        # ------------------------------------------------------------------------
        # Linked list node for markers
        # marker: ProToolsMarker   - the marker data
        # end: ProToolsMarker      - if there is a marker between this and the next marker marking the end of a segment
        # next: MarkerNode         - the next marker in the list
        def __init__(self, marker: ProToolsMarker):
            self.marker : ProToolsMarker = marker
            self.end : ProToolsMarker = None
            self.next : ProToolsMarkerManager.MarkerNode = None
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # Get the end of the segment
        ## returns: ProToolsMarker
        def get_end(self) -> ProToolsMarker:
            # If there is no end marker, return the next marker
            if self.end == None and self.next != None:
                return self.next.marker
            
            return self.end
        # ------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Pro Tools Marker Manager
    # filename: str    - the name of the file containing the Pro Tools Marker data
    def __init__(self, head_node: MarkerNode, frame_rate: float):
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
    def from_file(filename: str) -> 'ProToolsMarkerManager':
        with open(filename, 'r') as timecode_file:
            content = timecode_file.readlines()

            ## Get frame rate
            _, frame_rate = re.split(r"\t", content[PT_FRAMERATE_INDEX])
            frame_rate, _ = re.split("\s", frame_rate, 1)
            frame_rate = float(frame_rate)

            ## Get column headers
            header_data = re.split(r"\t", content[PT_COLUMN_HEADERS])
            column_headers = {header_data[i].strip() : i for i in range(len(header_data))}

            ## Check for required fields
            assert PT_MARKER_ID in column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_MARKER_ID}"
            assert PT_LOCATION_ID in column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_LOCATION_ID}"
            assert PT_TIMEREF_ID in column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_TIMEREF_ID}"
            assert PT_UNITS_ID in column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_UNITS_ID}"
            assert PT_NAME_ID in column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_NAME_ID}"
            assert PT_COMMENTS_ID in column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_COMMENTS_ID}"

            ## Create head node for linked list
            head_node = ProToolsMarkerManager.MarkerNode(ProToolsMarker.add_new_marker(content[PT_MARKER_DATA_START]))
            current_node = head_node

            ## Add markers to linked list
            for line in content[PT_MARKER_DATA_START+1:]:
                next_marker = ProToolsMarker.add_new_marker(line)

                # If the next marker is the end of a segment, set the current node's end to the next marker
                # Otherwise, add the next marker to the linked list
                if next_marker.name in ['x', 'END'] or \
                   (next_marker.name == 'w' and current_node.end == None):

                    current_node.end = next_marker
                else:
                    current_node.next = ProToolsMarkerManager.MarkerNode(next_marker)
                    current_node = current_node.next
            
            ## Create ProToolsMarkerManager
            return ProToolsMarkerManager(head_node, frame_rate)
        

    # ----------------------------------------------------------------------------
    # Create a ProToolsMarkerManager from a dictionary of timecodes
    # timecodes: dict    - the dictionary of timecodes
    ## returns: ProToolsMarkerManager
    @staticmethod
    def from_script(timecodes: dict) -> 'ProToolsMarkerManager':
        make_node = lambda key: ProToolsMarkerManager.MarkerNode(ProToolsMarker(key, timecodes[key] + ":00", None, None, key, 24.0))
        time_iter = iter(timecodes)
        key = next(time_iter)
        head_node = make_node(key)
        current_node = head_node

        for key in time_iter:
            next_node = make_node(key)
            current_node.next = next_node
            current_node = next_node
        
        current_node.next = ProToolsMarkerManager.MarkerNode(ProToolsMarker(len(timecodes.keys()), str(current_node.marker.timecode + 1), None, None, "END", 24.0))

        return ProToolsMarkerManager(head_node, 24.0)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Get the current node in the list and move to the next node
    ## returns: ProToolsMarker
    def get_current_node(self) -> MarkerNode:
        if self.current_node == None:
            return None
        
        node = self.current_node
        self.current_node = self.current_node.next

        return node
    # ----------------------------------------------------------------------------
    
# ================================================================================================