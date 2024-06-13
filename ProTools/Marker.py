
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
from enum import Enum
from ProTools.Timecode import Timecode, validate_frame_rate

# TODO: Add functionality for different Pro Tools Versions

# Delimiters
ROW_DELIMITER = r"\t"

# Starting Values
# TODO: Change the session start to match what is in Pro Tools
SESSION_START = Timecode.from_string("00:00:00:00")

# Error Messages
INVALID_COLUMN = f"Column {0} does not exist"

# TODO: Add in Marker ID max
INVALID_ID = "Marker {id}: ID cannot be less than 0"
INVALID_LOCATION = "Marker {id}: Location cannot be less than the session start time"
INVALID_NAME = "Marker {id}: Name cannot be empty"
INVALID_UNITS = "Marker{id}: Unit type {units} does not exist"

# ----------------------------------------------------------------------

# Marker Column Headers
class ColumnHeaders(Enum):
    ID = "#"
    LOCATION = "LOCATION"
    TIME_REFERENCE = "TIME REFERENCE"
    UNITS = "UNITS"
    NAME = "NAME"
    TRACK_NAME = "TRACK NAME"
    TRACK_TYPE = "TRACK TYPE"
    COMMENTS = "COMMENTS"

class Units(Enum):
    SAMPLES = "Samples"

class Marker:
    def __init__(self, id: int, location: Timecode, time_reference: str,
                 units: Units, name: str, comments: str = "",
                 frame_rate: float = 24.0):
        """Constructor for the Marker class
        
        Keyword arguments:
        id: str -- the ID of the marker
        location: str -- the location of the marker
        time_reference: str -- the time reference of the marker
        units: str -- the units of the marker
        name: str -- the name of the marker
        comments: str -- the comments of the marker (default "")
        frame_rate: float -- the frame rate of the marker (default 24.0)
        """

        assert id >= 0, INVALID_ID.format(id=id)
        assert location >= SESSION_START, INVALID_LOCATION.format(id=id)
        assert units in Units, INVALID_UNITS.format(id=id, units=units)
        assert name != None and name != "", INVALID_NAME.format(id=id)
        validate_frame_rate(frame_rate)

        self.id = id
        self.time_reference = time_reference
        self.units = units
        self.name = name
        self.frame_rate = frame_rate
        self.location = location
        self.comments = comments

    @classmethod
    def from_row(cls, column_headers: dict, row: str, frame_rate: float):
        """Create a new Marker object from a line of Pro Tools Marker data
        
        Keyword arguments:
        column_headers: dict
        row: str -- the line of text containing the marker data
        frame_rate: float
        """

        for header in column_headers.keys():
            assert header in ColumnHeaders, INVALID_COLUMN.format(header)
        validate_frame_rate(frame_rate)

        split_row = re.split(ROW_DELIMITER, row)
        row_values = [value.strip() for value in split_row] # Remove any leading or trailing whitespace

        get_row_value = lambda header: row_values[column_headers[header]]

        id = int(get_row_value(ColumnHeaders.ID))
        location = Timecode.from_string(get_row_value(ColumnHeaders.LOCATION))
        time_reference = int(get_row_value(ColumnHeaders.TIME_REFERENCE))
        units = Units(get_row_value(ColumnHeaders.UNITS))
        name = get_row_value(ColumnHeaders.NAME)
        comments = get_row_value(ColumnHeaders.COMMENTS)

        return cls(id, location, time_reference, units, name, frame_rate, comments)

    # OPERATORS

    def __eq__(self, other):
        """Compare two Marker objects to determine if they are equal"""

        if isinstance(other, Marker):
            return (self.id == other.id and
                    self.location == other.location and
                    self.time_reference == other.time_reference and
                    self.units == other.units and
                    self.name == other.name and
                    self.comments == other.comments)
        
        return False

    def __ne__(self, other):
        """Compare two Marker objects to determine if they are not equal"""
        
        return not self.__eq__(other)
