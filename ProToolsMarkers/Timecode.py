# TODO: Add support for timecode with hours

ROUNDING_RATE = 0.5                                 # Determine whether to round up or down
TIMECODE_IN_FRAMES = "{0:02d}:{1:02d}:{2:02d}:{3:02d}"   # Timecode in frames
TIMECODE_IN_MS = "{0:02d}:{1:02d}:{2:02d},{3:03d}"       # Timecode in milliseconds

class Timecode:

    # TODO: Refactor the initializer to be compliant with Python
    #       Look at this Stack Overflow post for guidance:
    #       https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python


    """
    Constructor based on separate time components
    hours: int      - the number of hours
    minutes: int    - the number of minutes
    seconds: int    - the number of seconds
    frames: int     - the number of frames
    frame_rate: float- the number of frames per second
    """
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0, frames: int = 0, frame_rate: float = 24.0):
        assert 0 <= hours, "Hours must be greater than or equal to 0"
        assert 0 <= minutes < 60, "Minutes must be between 0 and 59"
        assert 0 <= seconds < 60, "Seconds must be between 0 and 59"
        assert 0 <= frames < frame_rate, "Frames must be between 0 and the frame rate"
        assert 0 < frame_rate, "Frame rate must be greater than 0"
        
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames
        self.frame_rate = frame_rate


    """
    Constructor based on total number of frames
    x: int|str           - the total number of frames OR a string formatted as HH:MM:SS:FF
    frame_rate: float    - the number of frames per second
    """
    @classmethod
    def from_frames(cls, x, frame_rate: float = 24.0):
        if type(x) == int:
            assert 0 <= x, "Frames must be greater than or equal to 0"
            frames = int(x % frame_rate)
            x //= frame_rate
            seconds = int(x % 60)
            x //= 60
            minutes = int(x % 60)
            x //= 60
            hours = int(x % 60)
        elif type(x) == str:
            assert len(x) == 11 and x[2] == ":" and x[5] == ":" and x[8] == ":", "Invalid timecode format"
            hours, minutes, seconds, frames = map(int, x.split(":"))
        else:
            raise TypeError("Invalid arguments for Timecode.from_frames")
        return cls(hours, minutes, seconds, frames, frame_rate)


    """
    Convert the timecode to the total number of frames
    """
    def get_total_frames(self) -> int:
        total_seconds = (self.hours * 60 + self.minutes) * 60 + self.seconds
        return int(total_seconds * self.frame_rate + self.frames)
    

    def __str__(self):
        return self.get_timecode_in_frames()


    """
    Convert the timecode to a string formatted as HH:MM:SS:FF
    """
    def get_timecode_in_frames(self) -> str:
        return TIMECODE_IN_FRAMES.format(self.hours, self.minutes, self.seconds, self.frames)


    """
    Convert the timecode to a string formatted as HH:MM:SS,mmm
    """
    def get_timecode_in_ms(self) -> str:
        ms = int((self.frames * 1000) / self.frame_rate + ROUNDING_RATE)
        return TIMECODE_IN_MS.format(self.hours, self.minutes, self.seconds, ms)
    

    """
    This section overrides the various comparison operators
    """
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
    

    """
    This section overrides the various arithmetic operators
    """
    def __add__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() + other.get_total_frames()
            return Timecode.from_frames(total_frames, self.frame_rate)
        elif isinstance(other, int):
            total_frames = self.get_total_frames() + other
            return Timecode.from_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__add__")

    def __sub__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() - other.get_total_frames()
            return Timecode.from_frames(total_frames, self.frame_rate)
        elif isinstance(other, int):
            total_frames = self.get_total_frames() - other
            return Timecode.from_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__sub__")
    
    def __mul__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() * other
            return Timecode.from_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__mul__")
    
    def __truediv__(self, other):
        if isinstance(other, int):
            total_frames = int(self.get_total_frames() / other)
            return Timecode.from_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__truediv__")
    
    def __floordiv__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() // other
            return Timecode.from_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__floordiv__")
    
    def __mod__(self, other):
        if isinstance(other, int):
            total_frames = self.get_total_frames() % other
            return Timecode.from_frames(total_frames, self.frame_rate)
        
        raise TypeError("Invalid arguments for Timecode.__mod__")
    