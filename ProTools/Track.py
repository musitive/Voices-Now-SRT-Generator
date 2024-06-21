from enum import Enum

from ProTools.EDL import EDL
import ProTools.lib as lib

class States(Enum):
    MUTED = "Muted"
    UNMUTED = "Unmuted"

class Track:
    def __init__(self, name: str, comments: str, user_delay: str, state: States,
                 plugins: list, channels: list[EDL]):
        """Constructor for the Track class

        Keyword arguments:
        name: str -- the name of the Pro Tools Track
        comments: str -- the comments of the Pro Tools Track
        user_delay: str -- the user delay of the Pro Tools Track
        state: States -- the state of the Pro Tools Track
        channels: list[EDL] -- the list of EDLs in the Pro Tools Track
        """

        self.name = name
        self.comments = comments
        self.user_delay = user_delay
        self.state = state
        self.channels = channels

    @classmethod
    def from_rows(cls, column_headers: list, rows: list[str], frame_rate: float = 24.0):
        """Constructor for the Track class from a list of rows
        
        Keyword arguments:
        rows: list[str] -- the rows of the Pro Tools Track
        frame_rate: float -- the frame rate of the Pro Tools session (default: 24.0)
        """

        NAME_INDEX = 0
        COMMENTS_INDEX = 1
        USER_DELAY_INDEX = 2
        STATE_INDEX = 3
        # PLUGINS_INDEX = 4
        COLUMN_HEADERS_INDEX = 4

        name = rows[NAME_INDEX]
        comments = rows[COMMENTS_INDEX]
        user_delay = rows[USER_DELAY_INDEX]
        state = None
        plugins = None

        # TODO: Check headers

        channels: list[list[EDL]] = []
        current_channel: list[EDL] = []

        for line_index in range(COLUMN_HEADERS_INDEX+1, len(rows)):
            row = rows[line_index]
            if row == "":
                channels.append(current_channel)
                current_channel = []
                line_index += 1
                continue
            else:
                current_channel.append(EDL.from_row(column_headers, row))
        
        channels.append(current_channel)

        return cls(name, comments, user_delay, state, plugins, channels)