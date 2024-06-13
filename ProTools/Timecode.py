import re
from enum import Enum

# Rates
ROUNDING_RATE = 0.5
MILLISECONDS_PER_SECOND = 1000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60

# Delimiters
STANDARD_TIME_DELIMITER = ":"
DROP_FRAME_DELIMITER = ";"
STANDARD_MILLISECONDS_DELIMITER = ","
ALTERNATE_MILLISECONDS_DELIMITER = "."

# Formats
FRAMES_FORMAT = "{0:02d}:{1:02d}:{2:02d}:{3:02d}"
MILLISECONDS_FORMAT = "{0:02d}:{1:02d}:{2:02d},{3:03d}"
DROP_FRAME_FORMAT = "{0:02d}:{1:02d}:{2:02d};{3:02d}"

# Validation Regular Expressions
FRAMES_REGEX = r"^\d{2}:\d{2}:\d{2}:\d{2}$"
MILLISECONDS_REGEX = r"^\d{2}:\d{2}:\d{2}[,.]\d{3}$"
DROP_FRAME_REGEX = r"^\d{2}:\d{2}:\d{2};\d{2}$"

# Indices
DELIMITER_INDEX = 8

# Defaults
DEFAULT_FRAME_RATE = 24.0
DEFAULT_DROP_FRAME = False

# Error Messages
INVALID_HOURS = "Hours must be greater than or equal to 0"
INVALID_MINUTES = "Minutes must be between 0 and 59"
INVALID_SECONDS = "Seconds must be between 0 and 59"
INVALID_FRAME_RATE = "Frame rate must be greater than 0"
INVALID_MILLISECONDS = "Milliseconds must be between 0 and 999"
INVALID_TOTAL_FRAMES = "Total frames must be greater than or equal to 0"

INVALID_TYPE = f"Timecode must be {0}"

NO_MATCH = "No matching timecode format found"
INVALID_FRAME_FORMAT = "Timecode must be formatted as HH:MM:SS:FF"
INVALID_DROP_FRAME_FORMAT = "Timecode must be formatted as HH:MM:SS;FF"
INVALID_MILLISECONDS_FORMAT = "Timecode must be formatted as HH:MM:SS,mmm or HH:MM:SS.mmm"

class OffsetType(Enum):
    NONE = 0
    ADVANCE = 1
    DELAY = 2

class TimecodeOrder(Enum):
    HOURS = 0,
    MINUTES = 1,
    SECONDS = 2,
    FRAMES = 3,
    MILLISECONDS = 3 # Shared with frames

# TODO: check drop frame arithmetic
# TODO: consider reworking the class to use a single time component

class Timecode:
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0,
                 frames: int = 0, frame_rate: float = DEFAULT_FRAME_RATE,
                 drop_frame: bool = DEFAULT_DROP_FRAME):
        """Constructor for the Timecode class
        
        Keyword arguments:
        hours: int -- the number of hours (default 0)
        minutes: int -- the number of minutes (default 0)
        seconds: int -- the number of seconds (default 0)
        frames: int -- the number of frames (default 0)
        frame_rate: float -- the number of frames per second (default 24.0)
        drop_frame: bool -- whether to use drop frame arithmetic (default False)
        """
        
        assert 0 <= hours, INVALID_HOURS
        assert 0 <= minutes < MINUTES_PER_HOUR, INVALID_HOURS
        assert 0 <= seconds < SECONDS_PER_MINUTE, INVALID_SECONDS

        # TODO: fix this assertion
        # if not drop_frame: assert 0 <= frames < frame_rate, "Frames must be between 0 and the frame rate"
        assert 0 < frame_rate, INVALID_FRAME_RATE
        
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames
        self.frame_rate = frame_rate
        self.drop_frame = drop_frame


    @classmethod
    def from_total_frames(cls, total_frames: int, 
                          frame_rate: float = DEFAULT_FRAME_RATE,
                          drop_frame: bool = DEFAULT_DROP_FRAME):
        """Constructor for the Timecode class based on the total
           number of frames
           
        Keyword arguments:
        total_frames: int -- the total number of frames
        frame_rate: float -- the number of frames per second (default 24.0)
        drop_frame: bool -- whether to use drop frame arithmetic (default False)
        """

        assert type(total_frames) == int, INVALID_TYPE.format("an integer")
        assert 0 <= total_frames, INVALID_TOTAL_FRAMES

        frames = int(total_frames % frame_rate)
        remaining_frames = total_frames // frame_rate

        seconds = int(remaining_frames % SECONDS_PER_MINUTE)
        remaining_frames //= SECONDS_PER_MINUTE

        minutes = int(remaining_frames % SECONDS_PER_MINUTE)
        remaining_frames //= MINUTES_PER_HOUR

        hours = int(remaining_frames % MINUTES_PER_HOUR)

        return cls(hours, minutes, seconds, frames, frame_rate, drop_frame)


    @classmethod
    def from_string(cls, timecode: str,
                    frame_rate: float = DEFAULT_FRAME_RATE):
        """Constructor for the Timecode class based on a string
        
        Keyword arguments:
        timecode: str -- the timecode formatted as on of the following:
                            - HH:MM:SS:FF
                            - HH:MM:SS,mmm
                            - HH:MM:SS;FF
        frame_rate: float -- the number of frames per second (default 24.0)
        """
        
        assert type(timecode) == str, INVALID_TYPE.format("a string")
        assert 0 < frame_rate, INVALID_FRAME_RATE

        if re.match(FRAMES_REGEX, timecode):
            hours, minutes, seconds, frames = map(int, timecode.split(STANDARD_TIME_DELIMITER))
            return cls(hours, minutes, seconds, frames, frame_rate)
        
        elif re.match(MILLISECONDS_REGEX, timecode):
            return Timecode.from_milliseconds_format(timecode, frame_rate)
        
        elif re.match(DROP_FRAME_REGEX, timecode):
            return Timecode.from_drop_frame_format(timecode, frame_rate)

        else:
            raise ValueError("Invalid timecode format")


    @classmethod
    def from_frame_format(cls, timecode: str,
                          frame_rate: float = DEFAULT_FRAME_RATE):
        """Constructor for the Timecode class based on a string
           formatted as HH:MM:SS:FF
           
        Keyword arguments:
        timecode: str -- the timecode formatted as HH:MM:SS:FF
        frame_rate: float -- the number of frames per second (default 24.0)
        """

        assert type(timecode) == str, INVALID_TYPE.format("a string")
        assert 0 < frame_rate, INVALID_FRAME_RATE
        assert re.match(FRAMES_REGEX, timecode), INVALID_FRAME_FORMAT

        hours, minutes, seconds, frames = Timecode.split_string(timecode)

        return cls(hours, minutes, seconds, frames, frame_rate)


    @classmethod
    def from_drop_frame_format(cls, timecode: str,
                               frame_rate: float = DEFAULT_FRAME_RATE):
        """Constructor for the Timecode class based on a string
           formatted as HH:MM:SS;FF
        
        Keyword arguments:
        timecode: str -- the timecode formatted as HH:MM:SS;FF
        frame_rate: float -- the number of frames per second (default 24.0)
        """
        
        assert type(timecode) == str, INVALID_TYPE.format("a string")
        assert re.match(DROP_FRAME_REGEX, timecode), INVALID_DROP_FRAME_FORMAT
        assert 0 < frame_rate, INVALID_FRAME_RATE

        hours, minutes, seconds, frames = Timecode.split_string(timecode)

        return cls(hours, minutes, seconds, frames, frame_rate, True)


    @classmethod
    def from_milliseconds_format(cls, timecode: str,
                          frame_rate: float = DEFAULT_FRAME_RATE):
        """Constructor for the Timecode class based on a string
           formatted as HH:MM:SS,mmm or HH:MM:SS.mmm
        
        Keyword arguments:
        timecode: str -- the timecode formatted as HH:MM:SS,mmm or HH:MM:SS.mmm
        frame_rate: float -- the number of frames per second (default 24.0)
        """
        
        assert type(timecode) == str, INVALID_TYPE.format("a string")
        assert re.match(MILLISECONDS_REGEX, timecode), INVALID_MILLISECONDS_FORMAT
        assert 0 < frame_rate, INVALID_FRAME_RATE

        hours, minutes, seconds, milliseconds = Timecode.split_string(timecode)

        return cls(hours, minutes, seconds, milliseconds, frame_rate)


    @staticmethod
    def split_string(timecode: str) -> list:
        """Split the timecode string into its components
        
        Keyword arguments:
        timecode: str -- the timecode formatted as HH:MM:SS:FF
        """

        assert type(timecode) == str, INVALID_TYPE.format("a string")
        assert re.match(FRAMES_REGEX, timecode) or \
                re.match(MILLISECONDS_REGEX, timecode) or \
                re.match(DROP_FRAME_REGEX, timecode), NO_MATCH

        delimiter = timecode[DELIMITER_INDEX]
        split_timecode = timecode.split(STANDARD_TIME_DELIMITER)

        hours = int(split_timecode[TimecodeOrder.HOURS.value])
        minutes = int(split_timecode[TimecodeOrder.MINUTES.value])

        if delimiter == STANDARD_TIME_DELIMITER:
            seconds = int(split_timecode[TimecodeOrder.SECONDS.value])
            end_value = int(split_timecode[TimecodeOrder.FRAMES.value])
        else:
            remaining_time = split_timecode[TimecodeOrder.SECONDS.value]
            remaining_values = remaining_time.split(delimiter)
            seconds = int(remaining_values[0])
            end_value = int(remaining_values[1])
        
        return hours, minutes, seconds, end_value


    @staticmethod
    def milliseconds_to_frames(milliseconds: int,
                               frame_rate: float = DEFAULT_FRAME_RATE) -> int:
        """Convert milliseconds to frames

        Keyword arguments:
        milliseconds: int -- the number of milliseconds
        frame_rate: float -- the number of frames per second
        """

        assert type(milliseconds) == int, INVALID_TYPE.format("an integer")
        assert milliseconds >= 0 and \
            milliseconds < MILLISECONDS_PER_SECOND, INVALID_MILLISECONDS
        assert 0 < frame_rate, INVALID_FRAME_RATE

        seconds_as_decimal = milliseconds / MILLISECONDS_PER_SECOND
        frames = int(seconds_as_decimal * frame_rate + ROUNDING_RATE)

        return frames


    @staticmethod
    def frames_to_milliseconds(frames: int,
                               frame_rate: float = DEFAULT_FRAME_RATE) -> int:
        """Convert frames to milliseconds
        
        Keyword arguments:
        frames: int -- the number of frames
        frame_rate: float -- the number of frames per second
        """

        assert frames >= 0, INVALID_TOTAL_FRAMES
        assert 0 < frame_rate, INVALID_FRAME_RATE

        seconds_as_decimal = frames / frame_rate
        milliseconds = int(seconds_as_decimal * MILLISECONDS_PER_SECOND + ROUNDING_RATE)

        return milliseconds


    def get_total_frames(self) -> int:
        """Convert the timecode to the total number of frames"""

        total_minutes = int(self.hours * MINUTES_PER_HOUR + self.minutes)
        total_seconds = int(total_minutes * SECONDS_PER_MINUTE + self.seconds)
        total_frames = int(total_seconds * self.frame_rate + self.frames)

        return total_frames


    def convert_to_frames_format(self) -> str:
        """Convert the timecode to a string formatted as HH:MM:SS:FF"""

        timecode_format = FRAMES_FORMAT if not self.drop_frame else DROP_FRAME_FORMAT

        return timecode_format.format(self.hours, self.minutes, self.seconds, self.frames)


    def convert_to_milliseconds_format(self) -> str:
        """Convert the timecode to a string formatted as HH:MM:SS,mmm"""

        milliseconds = Timecode.frames_to_milliseconds(self.frames, self.frame_rate)

        return MILLISECONDS_FORMAT.format(self.hours, self.minutes, self.seconds, milliseconds)


    def __str__(self):
        return self.convert_to_frames_format()


    # COMPARISON OPERATORS

    def __eq__(self, other):
        if isinstance(other, Timecode):
            return (self.hours == other.hours and
                    self.minutes == other.minutes and
                    self.seconds == other.seconds and
                    self.frames == other.frames and
                    self.frame_rate == other.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__eq__")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Timecode):
            return self.get_total_frames() < other.get_total_frames()
        
        raise TypeError("Invalid arguments for Timecode.__lt__")

    def __le__(self, other):    
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):    
        return not self.__le__(other)

    def __ge__(self, other):    
        return not self.__lt__(other)

    # ARITHMETIC OPERATORS

    def __add__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() + other.get_total_frames()
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        elif isinstance(other, int):
            total_frames = self.get_total_frames() + other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__add__")

    def __sub__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() - other.get_total_frames()
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        elif isinstance(other, int):
            total_frames = self.get_total_frames() - other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__sub__")

    def __mul__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() * other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__mul__")

    def __truediv__(self, other):
        if isinstance(other, int):
            total_frames = int(self.get_total_frames() / other)
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__truediv__")

    def __floordiv__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() // other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__floordiv__")

    def __mod__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() % other
            return Timecode.from_total_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__mod__")