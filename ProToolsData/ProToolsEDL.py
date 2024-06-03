"""
EXAMPLE PRO TOOLS EDL

CHANNEL 	EVENT   	CLIP NAME                     	START TIME    	END TIME      	DURATION      	STATE
1       	1       	1            	                01:00:21:17	    01:00:34:07	    00:00:12:14	    Unmuted

"""

import re
from ProToolsData.Timecode import Timecode

# ================================================================================================

# Pro Tools EDL data IDs
PT_CHANNEL_ID = "CHANNEL"
PT_EVENT_ID = "EVENT"
PT_CLIP_ID = "CLIP NAME"
PT_START_ID = "START TIME"
PT_END_ID = "END TIME"
PT_DURATION_ID = "DURATION"
PT_STATE_ID = "STATE"

PT_COLUMN_HEADERS = [PT_CHANNEL_ID, PT_EVENT_ID, PT_CLIP_ID, PT_START_ID, PT_END_ID, PT_DURATION_ID, PT_STATE_ID]

# ================================================================================================

class ProToolsEDL:
    # ----------------------------------------------------------------------------
    # Pro Tools EDL
    # channel: str       - the channel of the EDL
    # event: str         - the event of the EDL
    # clip_name: str     - the name of the clip
    # start_time: str    - the start time of the clip
    # end_time: str      - the end time of the clip
    # duration: str      - the duration of the clip
    # state: str         - the state of the clip
    # frame_rate: float  - the frame rate of the clip
    def __init__(self, channel: str, event: str, clip_name: str, start_time: str, end_time: str, duration: str, state: str, frame_rate: float):
        
        # Validate input
        assert event != "" and int(event) >= 0, f"Invalid ProTools Marker ID: {event}"

        assert clip_name != "", f"ProTools Marker name cannot be empty at ProTools Marker {event}"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        # Set attributes
        self.channel = channel
        self.event = event
        self.loop = clip_name
        self.start_time = Timecode.from_frames(start_time, frame_rate)
        self.end_time = Timecode.from_frames(end_time, frame_rate)
        self.duration = Timecode.from_frames(duration, frame_rate)
        self.state = state

        # TODO: rewrite this so it knows how to better handle the hours
        self.start_time.hours = 0
        self.end_time.hours = 0
        self.duration.hours = 0
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Static method to create a new ProToolsEDL object from a line of text
    # column_headers: dict  - the column headers of the EDL data
    # line: str             - the line of text containing the marker data
    # frame_rate: float     - the frame rate of the Pro Tools session
    ## returns: ProToolsMarker
    @staticmethod
    def create_new_EDL(column_headers: dict, line: str, frame_rate: float) -> 'ProToolsEDL':
        # Split the line into marker data
        edl_data = re.split(r"\t", line)
        edl_data = [x.strip() for x in edl_data]

        # Verify that the marker data is complete
        try:
            channel = edl_data[column_headers[PT_CHANNEL_ID]]
            event = edl_data[column_headers[PT_EVENT_ID]]
            clip_name = edl_data[column_headers[PT_CLIP_ID]]
            start_time = edl_data[column_headers[PT_START_ID]]
            end_time = edl_data[column_headers[PT_END_ID]]
            duration = edl_data[column_headers[PT_DURATION_ID]]
            state = edl_data[column_headers[PT_STATE_ID]]
        except KeyError as e:
            raise(f"Error: Pro Tools Marker data is missing a required field: {e}")

        return ProToolsEDL(channel, event, clip_name, start_time, end_time, duration, state, frame_rate)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Compare two ProToolsMarker objects to determine if they are equal
    def __eq__(self, other):
        if isinstance(other, ProToolsEDL):
            return (self.channel == other.channel and
                    self.event == other.event and
                    self.loop == other.loop and
                    self.start_time == other.start_time and
                    self.end_time == other.end_time and
                    self.duration == other.duration and
                    self.state == other.state)
        
        return False
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Compare two ProToolsMarker objects to determine if they are not equal
    def __ne__(self, other):
        return not self.__eq__(other)
    # ----------------------------------------------------------------------------
    
# ================================================================================================