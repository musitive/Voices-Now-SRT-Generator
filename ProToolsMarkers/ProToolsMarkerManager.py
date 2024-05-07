"""
Code to extract Pro Tools Markers
Author: Dallin Frank

Run test cases:
py -m unittest TestProToolsMarkerManager
"""

from ProToolsMarkers.ProToolsMarker import ProToolsMarker
import re

# ================================================================================================

# --------------------------------------------------------------------------------
# Indices for Pro Tools Marker data
PT_COLUMN_HEADERS = 11
PT_MARKER_DATA_START = 12
PT_FRAMERATE_INDEX = 4
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Pro Tools Marker data column headers
PT_MARKER_ID = "#"
PT_LOCATION_ID = "LOCATION"
PT_TIMEREF_ID = "TIME REFERENCE"
PT_UNITS_ID = "UNITS"
PT_NAME_ID = "NAME"
PT_TNAME_ID = "TRACK NAME"
PT_TTYPE_ID = "TRACK TYPE"
PT_COMMENTS_ID = "COMMENTS"
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
    def __init__(self, filename: str):
        with open(filename, 'r') as timecode_file:
            content = timecode_file.readlines()

            ## Get frame rate
            _, frame_rate = re.split(r"\t", content[PT_FRAMERATE_INDEX])
            frame_rate, _ = re.split("\s", frame_rate, 1)
            self.FRAME_RATE = float(frame_rate)

            ## Get column headers
            header_data = re.split(r"\t", content[PT_COLUMN_HEADERS])
            self.column_headers = {header_data[i].strip() : i for i in range(len(header_data))}

            ## Check for required fields
            assert PT_MARKER_ID in self.column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_MARKER_ID}"
            assert PT_LOCATION_ID in self.column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_LOCATION_ID}"
            assert PT_TIMEREF_ID in self.column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_TIMEREF_ID}"
            assert PT_UNITS_ID in self.column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_UNITS_ID}"
            assert PT_NAME_ID in self.column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_NAME_ID}"
            assert PT_COMMENTS_ID in self.column_headers, f"Error: Pro Tools Marker data is missing a required field: {PT_COMMENTS_ID}"

            ## Create head node for linked list
            self.head_node = ProToolsMarkerManager.MarkerNode(self.add_new_marker(content[PT_MARKER_DATA_START]))
            current_node = self.head_node

            ## Add markers to linked list
            for line in content[PT_MARKER_DATA_START+1:]:
                next_marker = self.add_new_marker(line)

                # If the next marker is the end of a segment, set the current node's end to the next marker
                # Otherwise, add the next marker to the linked list
                if next_marker.name in ['x', 'END'] or \
                   (next_marker.name == 'w' and current_node.end == None):

                    current_node.end = next_marker
                else:
                    current_node.next = ProToolsMarkerManager.MarkerNode(next_marker)
                    current_node = current_node.next
            
            ## Set current node to head node
            self.current_node = self.head_node
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Add a new marker to the list of markers
    # line: str       - the line of text containing the marker data
    ## returns: ProToolsMarker 
    def add_new_marker(self, line: str) -> ProToolsMarker:
        # Split the line into marker data
        marker_data = re.split(r"\t", line)
        marker_data = [x.strip() for x in marker_data]

        # Verify that the marker data is complete
        try:
            marker_id = marker_data[self.column_headers[PT_MARKER_ID]]
            location = marker_data[self.column_headers[PT_LOCATION_ID]]
            time_reference = marker_data[self.column_headers[PT_TIMEREF_ID]]
            units = marker_data[self.column_headers[PT_UNITS_ID]]
            name = marker_data[self.column_headers[PT_NAME_ID]]
            comments = marker_data[self.column_headers[PT_COMMENTS_ID]]
        except KeyError as e:
            raise(f"Error: Pro Tools Marker data is missing a required field: {e}")

        return ProToolsMarker(marker_id, location, time_reference, units, name, self.FRAME_RATE, comments)
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