import re
from enum import Enum

# Rates
ROUNDING_RATE = 0.5
MILLISECONDS_PER_SECOND = 1000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60

# Formats
FRAMES_FORMAT = "{0:02d}:{1:02d}:{2:02d}:{3:02d}"
MILLISECONDS_FORMAT = "{0:02d}:{1:02d}:{2:02d},{3:03d}"
DROP_FRAME_FORMAT = "{0:02d}:{1:02d}:{2:02d};{3:02d}"

# Delimiters
STANDARD_TIME_DELIMITER = ":"
DROP_FRAME_DELIMITER = ";"
STANDARD_MILLISECONDS_DELIMITER = ","
ALTERNATE_MILLISECONDS_DELIMITER = "."

# Validation Regular Expressions
FRAMES_REGEX = r"^\d{2}:\d{2}:\d{2}:\d{2}$"
MILLISECONDS_REGEX = r"^\d{2}:\d{2}:\d{2}[,.]\d{3}$"
DROP_FRAME_REGEX = r"^\d{2}:\d{2}:\d{2};\d{2}$"

# Defaults
DEFAULT_FRAME_RATE = 24.0
DEFAULT_DROP_FRAME = False

class OffsetType(Enum):
    NONE = 0
    ADVANCE = 1
    DELAY = 2

# TODO: check drop frame arithmetic
# TODO: consider reworking the class to use a single time component

class Timecode:
   
    # Constructor based on separate time components
    # hours: int      - the number of hours
    # minutes: int    - the number of minutes
    # seconds: int    - the number of seconds
    # frames: int     - the number of frames
    # frame_rate: float- the number of frames per second
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0, frames: int = 0,
                 frame_rate: float = DEFAULT_FRAME_RATE, drop_frame: bool = DEFAULT_DROP_FRAME):
        
        assert 0 <= hours, "Hours must be greater than or equal to 0"
        assert 0 <= minutes < MINUTES_PER_HOUR, "Minutes must be between 0 and 59"
        assert 0 <= seconds < SECONDS_PER_MINUTE, "Seconds must be between 0 and 59"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        # TODO: fix this assertion
        # if not drop_frame: assert 0 <= frames < frame_rate, "Frames must be between 0 and the frame rate"
        
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames
        self.frame_rate = frame_rate
        self.drop_frame = drop_frame


    # Constructor based on total number of frames
    # total_frames: int     - the total number of frames OR a string formatted as HH:MM:SS:FF
    # frame_rate: float     - the number of frames per second
    @classmethod
    def from_total_frames(cls, total_frames: int, frame_rate: float = DEFAULT_FRAME_RATE, drop_frame: bool = DEFAULT_DROP_FRAME):
        assert type(total_frames) == int, "Timecode must be a string or an integer"
        assert 0 <= total_frames, "Frames must be greater than or equal to 0"

        frames = int(total_frames % frame_rate)
        remaining_frames = total_frames // frame_rate

        seconds = int(remaining_frames % SECONDS_PER_MINUTE)
        remaining_frames //= SECONDS_PER_MINUTE

        minutes = int(remaining_frames % SECONDS_PER_MINUTE)
        remaining_frames //= MINUTES_PER_HOUR

        hours = int(remaining_frames % MINUTES_PER_HOUR)

        return cls(hours, minutes, seconds, frames, frame_rate, drop_frame)


    # Constructor based on a string formatted as HH:MM:SS:FF, HH:MM:SS,mmm or HH:MM:SS;FF
    # timecode: str        - the timecode formatted as HH:MM:SS:FF, HH:MM:SS,mmm or HH:MM:SS;FF
    # frame_rate: float    - the number of frames per second
    ## returns: Timecode
    @classmethod
    def from_string(cls, timecode: str, frame_rate: float = DEFAULT_FRAME_RATE):
        assert type(timecode) == str, "Timecode must be a string"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        if re.match(FRAMES_REGEX, timecode):
            hours, minutes, seconds, frames = map(int, timecode.split(STANDARD_TIME_DELIMITER))
            return cls(hours, minutes, seconds, frames, frame_rate)
        
        elif re.match(MILLISECONDS_REGEX, timecode):
            return Timecode.from_milliseconds(timecode, frame_rate)
        
        elif re.match(DROP_FRAME_REGEX, timecode):
            return Timecode.from_drop_frame(timecode, frame_rate)

        else:
            raise ValueError("Invalid timecode format")


    # Constructor based on a string formatted as HH:MM:SS;FF
    # timecode: str        - the timecode formatted as HH:MM:SS;FF
    # frame_rate: float    - the number of frames per second
    ## returns: Timecode
    @classmethod
    def from_drop_frame(cls, timecode: str, frame_rate: float = DEFAULT_FRAME_RATE):
        assert type(timecode) == str, "Timecode must be a string"
        assert re.match(DROP_FRAME_REGEX, timecode), "Timecode must be formatted as HH:MM:SS;FF"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        hours, minutes, seconds_and_frames = map(str, timecode.split(STANDARD_TIME_DELIMITER))
        hours = int(hours)
        minutes = int(minutes)
        seconds, frames = map(int, seconds_and_frames.split(DROP_FRAME_DELIMITER))

        return cls(hours, minutes, seconds, frames, frame_rate, drop_frame=True)


    # Constructor based on a string formatted as HH:MM:SS,mmm or HH:MM:SS.mmm
    # timecode: str        - the timecode formatted as HH:MM:SS,mmm or HH:MM:SS.mmm
    # frame_rate: float    - the number of frames per second
    ## returns: Timecode
    @classmethod
    def from_milliseconds(cls, timecode: str, frame_rate: float = DEFAULT_FRAME_RATE):
        assert type(timecode) == str, "Timecode must be a string"
        assert re.match(MILLISECONDS_REGEX, timecode), "Timecode must be formatted as HH:MM:SS,mmm or HH:MM:SS.mmm"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        hours, minutes, seconds_and_ms = map(str, timecode.split(STANDARD_TIME_DELIMITER))
        hours = int(hours)
        minutes = int(minutes)
        seconds, milliseconds = map(int, seconds_and_ms.split(STANDARD_MILLISECONDS_DELIMITER).split(ALTERNATE_MILLISECONDS_DELIMITER))
        frames = int((milliseconds * frame_rate) / MILLISECONDS_PER_SECOND + ROUNDING_RATE)

        return cls(hours, minutes, seconds, frames, frame_rate)


    # Convert milliseconds to frames
    # milliseconds: int     - the number of milliseconds
    # frame_rate: float     - the number of frames per second
    ## returns: int
    @staticmethod
    def milliseconds_to_frames(milliseconds: int, frame_rate: float = DEFAULT_FRAME_RATE) -> int:
        assert milliseconds >= 0 and milliseconds < MILLISECONDS_PER_SECOND, "Milliseconds must be between 0 and 999"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        seconds_as_decimal = milliseconds / MILLISECONDS_PER_SECOND
        frames = int(seconds_as_decimal * frame_rate + ROUNDING_RATE)

        return frames


    # Convert frames to milliseconds
    # frames: int           - the number of frames
    # frame_rate: float     - the number of frames per second
    ## returns: int
    @staticmethod
    def frames_to_milliseconds(frames: int, frame_rate: float = DEFAULT_FRAME_RATE) -> int:
        assert frames >= 0, "Frames must be greater than or equal to 0"
        assert 0 < frame_rate, "Frame rate must be greater than 0"

        seconds_as_decimal = frames / frame_rate
        milliseconds = int(seconds_as_decimal * MILLISECONDS_PER_SECOND + ROUNDING_RATE)

        return milliseconds


    # Convert the timecode to the total number of frames
    ## returns: int
    def get_total_frames(self) -> int:
        total_minutes = int(self.hours * MINUTES_PER_HOUR + self.minutes)
        total_seconds = int(total_minutes * SECONDS_PER_MINUTE + self.seconds)
        total_frames = int(total_seconds * self.frame_rate + self.frames)

        return total_frames


    # Convert the timecode to a string formatted as HH:MM:SS:FF
    ## returns: str
    def get_timecode_in_frames(self) -> str:
        if self.drop_frame:
            return DROP_FRAME_FORMAT.format(self.hours, self.minutes, self.seconds, self.frames)
        else:
            return FRAMES_FORMAT.format(self.hours, self.minutes, self.seconds, self.frames)


    # Convert the timecode to a string formatted as HH:MM:SS,mmm
    ## returns: str
    def get_timecode_in_ms(self) -> str:
        milliseconds = Timecode.frames_to_milliseconds(self.frames, self.frame_rate)
        return MILLISECONDS_FORMAT.format(self.hours, self.minutes, self.seconds, milliseconds)


    # To string
    def __str__(self):
        return self.get_timecode_in_frames()


    # --------------------------------------------------------------------------------
    # COMPARISON OPERATORS

    # Compare two Timecode objects to determine if they are equal
    def __eq__(self, other):
        if isinstance(other, Timecode):
            return (self.hours == other.hours and
                    self.minutes == other.minutes and
                    self.seconds == other.seconds and
                    self.frames == other.frames and
                    self.frame_rate == other.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__eq__")

    # Compare two Timecode objects to determine if they are not equal
    def __ne__(self, other):
        return not self.__eq__(other)

    # Compare two Timecode objects to determine if one is less than the other
    def __lt__(self, other):
        if isinstance(other, Timecode):
            return self.get_total_frames() < other.get_total_frames()
        
        raise TypeError("Invalid arguments for Timecode.__lt__")

    # Compare two Timecode objects to determine if one is less than or equal to the other
    def __le__(self, other):    
        return self.__lt__(other) or self.__eq__(other)

    # Compare two Timecode objects to determine if one is greater than the other
    def __gt__(self, other):    
        return not self.__le__(other)

    # Compare two Timecode objects to determine if one is greater than or equal to the other
    def __ge__(self, other):    
        return not self.__lt__(other)

    # --------------------------------------------------------------------------------
    # ARITHMETIC OPERATORS

    # Add Timecode object to either another Timecode object or an integer
    def __add__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() + other.get_total_frames()
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        elif isinstance(other, int):
            total_frames = self.get_total_frames() + other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__add__")

    # Subtract Timecode object from either another Timecode object or an integer
    def __sub__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() - other.get_total_frames()
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        elif isinstance(other, int):
            total_frames = self.get_total_frames() - other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__sub__")

    # Multiply Timecode object by an integer
    def __mul__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() * other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__mul__")

    # Divide Timecode object by an integer
    def __truediv__(self, other):
        if isinstance(other, int):
            total_frames = int(self.get_total_frames() / other)
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__truediv__")

    # Divide Timecode object by an integer and return the floor
    def __floordiv__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() // other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__floordiv__")

    # Divide Timecode object by an integer and return the remainder
    def __mod__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() % other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__mod__")