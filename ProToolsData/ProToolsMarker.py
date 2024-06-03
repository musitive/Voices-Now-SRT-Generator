
"""
EXAMPLE PRO TOOLS MARKER 1

#   	LOCATION     	TIME REFERENCE    	UNITS    	NAME                             	COMMENTS
1   	01:00:39:12  	2043360           	Samples  	1                                	

========================================================================================================================================================

EXAMPLE PRO TOOLS MARKER 2

#   	LOCATION     	TIME REFERENCE    	UNITS    	NAME                             	TRACK NAME                       	TRACK TYPE   	COMMENTS
1   	01:00:41:20  	2154152           	Samples  	1                                	Cues                             	Ruler                            	

"""

import re
from ProToolsData.Timecode import Timecode

# ================================================================================================

PT_MARKER_ID = "#"
PT_LOCATION_ID = "LOCATION"
PT_TIMEREF_ID = "TIME REFERENCE"
PT_UNITS_ID = "UNITS"
PT_NAME_ID = "NAME"
PT_TNAME_ID = "TRACK NAME"
PT_TTYPE_ID = "TRACK TYPE"
PT_COMMENTS_ID = "COMMENTS"

PT_COLUMN_HEADERS = [PT_MARKER_ID, PT_LOCATION_ID, PT_TIMEREF_ID, PT_UNITS_ID, PT_NAME_ID, PT_TNAME_ID, PT_TTYPE_ID, PT_COMMENTS_ID]

# ================================================================================================

class ProToolsMarker:
    # ----------------------------------------------------------------------------
    # Pro Tools Marker
    # marker_id: str         - the ID of the marker
    # location: str          - the location of the marker
    # time_reference: str    - the time reference of the marker
    # units: str             - the units of the marker
    # name: str              - the name of the marker
    # frame_rate: float      - the frame rate of the marker
    # comments: str          - the comments of the marker
    def __init__(self, marker_id: str, location: str, time_reference: str,
                 units: str, name: str, frame_rate: float, comments: str = ""):
        
        # Validate input
        assert marker_id != "" and int(marker_id) >= 0, f"Invalid ProTools Marker ID: {marker_id}"
        
        # assert int(time_reference) >= 0, f"Invalid location {time_reference} for ProTools Marker {marker_id}"
        # assert units == "Samples", f"Unit type {units} unsupported at ProTools Marker {marker_id}"
        assert name != "", f"ProTools Marker name cannot be empty at ProTools Marker {marker_id}"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        # Set attributes
        self.marker_id = marker_id
        self.time_reference = time_reference
        self.units = units
        self.name = name
        self.frame_rate = frame_rate
        self.timecode = Timecode.from_frames(location, frame_rate)
        self.comments = comments

        # TODO: rewrite this so it knows how to better handle the hours
        self.timecode.hours = 0
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Static method to create a new ProToolsMarker from a line of text
    # column_headers: dict  - the column headers for the Pro Tools Marker data
    # line: str             - the line of text containing the marker data
    # frame_rate: float     - the frame rate of the Pro Tools session
    ## returns: ProToolsMarker
    @staticmethod
    def create_new_marker(column_headers: dict, line: str, frame_rate: float) -> 'ProToolsMarker':
        # Split the line into marker data
        marker_data = re.split(r"\t", line)
        marker_data = [x.strip() for x in marker_data]

        # Verify that the marker data is complete
        try:
            marker_id = marker_data[column_headers[PT_MARKER_ID]]
            location = marker_data[column_headers[PT_LOCATION_ID]]
            time_reference = marker_data[column_headers[PT_TIMEREF_ID]]
            units = marker_data[column_headers[PT_UNITS_ID]]
            loop = marker_data[column_headers[PT_NAME_ID]]
            comments = marker_data[column_headers[PT_COMMENTS_ID]]
        except KeyError as e:
            raise(f"Error: Pro Tools Marker data is missing a required field: {e}")

        return ProToolsMarker(marker_id, location, time_reference, units, loop, frame_rate, comments)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Compare two ProToolsMarker objects to determine if they are equal
    def __eq__(self, other):
        if isinstance(other, ProToolsMarker):
            return (self.marker_id == other.marker_id and
                    self.timecode == other.timecode and
                    self.time_reference == other.time_reference and
                    self.units == other.units and
                    self.name == other.name and
                    self.comments == other.comments)
        
        return False
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Compare two ProToolsMarker objects to determine if they are not equal
    def __ne__(self, other):
        return not self.__eq__(other)
    # ----------------------------------------------------------------------------
    
# ================================================================================================