"""
EXAMPLE EDL

CHANNEL 	EVENT   	CLIP NAME                     	START TIME    	END TIME      	DURATION      	STATE
1       	1       	1            	                01:00:21:17	    01:00:34:07	    00:00:12:14	    Unmuted

"""

import re
from enum import Enum
from ProTools.Timecode import Timecode, validate_frame_rate
import ProTools.lib as lib

# Delimiters
ROW_DELIMITER = r"\t"

# Error Messages
INVALID_COLUMN = f"Column {0} does not exist"

INVALID_EVENT = "EDL {event}: Event cannot be less than 0"
INVALID_CLIP_NAME = "EDL {event}: Name cannot be empty"

class ColumnHeaders(Enum):
    CHANNEL = "CHANNEL"
    EVENT = "EVENT"
    CLIP_NAME = "CLIP NAME"
    START_TIME = "START TIME"
    END_TIME = "END TIME"
    DURATION = "DURATION"
    STATE = "STATE"

class States(Enum):
    MUTED = "Muted"
    UNMUTED = "Unmuted"

class EDL:
    def __init__(self, channel: int, event: int, clip_name: str,
                 start_time: Timecode, end_time: Timecode, duration: Timecode,
                 state: States, frame_rate: float = 24.0):
        """Constructor for the EDL class
        
        Keyword arguments:
        channel: int -- the channel of the Pro Tools Marker
        event: int -- the ID of the Pro Tools Marker
        clip_name: str -- the name of the Pro Tools Marker
        start_time: str -- the start time of the Pro Tools Marker
        end_time: str -- the end time of the Pro Tools Marker
        duration: str -- the duration of the Pro Tools Marker
        state: States -- the state of the Pro Tools Marker
        frame_rate: float -- the frame rate of the Pro Tools session (default: 24.0)
        """

        assert event >= 0, INVALID_EVENT.format(event=event)
        assert clip_name != None and clip_name != "", INVALID_CLIP_NAME.format(event=event)
        validate_frame_rate(frame_rate)

        self.channel = channel
        self.event = event
        self.loop = clip_name
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.state = state


    @classmethod
    def from_row(cls, column_headers: dict, row: str,
                       frame_rate: float = 24.0):
        """Construct a new EDL object from a row of Pro Tools EDL data
        
        Keyword arguments:
        column_headers: dict -- the column headers of the EDL data
        row: str -- the line of text containing the marker data
        frame_rate: float -- the frame rate of the Pro Tools session
        """

        for header in column_headers.keys():
            assert header in ColumnHeaders, INVALID_COLUMN.format(header)
        validate_frame_rate(frame_rate)

        row_values = lib.split_row(row)

        get_row_value = lambda header: row_values[column_headers[header]]
        create_timecode = lambda header: Timecode.from_string(get_row_value(header))

        channel = int(get_row_value(ColumnHeaders.CHANNEL))
        event = int(get_row_value(ColumnHeaders.EVENT))
        clip_name = get_row_value(ColumnHeaders.CLIP_NAME)
        state = States(get_row_value(ColumnHeaders.STATE))

        start_time = create_timecode(ColumnHeaders.START_TIME)
        end_time = create_timecode(ColumnHeaders.END_TIME)
        duration = create_timecode(ColumnHeaders.DURATION)

        return cls(channel, event, clip_name, start_time, end_time, duration,
                   state, frame_rate)


    def __eq__(self, other):
        """Compare two EDL objects to determine if they are equal"""
        if isinstance(other, EDL):
            return (self.channel == other.channel and
                    self.event == other.event and
                    self.loop == other.loop and
                    self.start_time == other.start_time and
                    self.end_time == other.end_time and
                    self.duration == other.duration and
                    self.state == other.state)
        
        return False
    
    def __ne__(self, other):
        """Compare two EDL objects to determine if they are not equal"""
        return not self.__eq__(other)