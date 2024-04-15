ROUNDING_RATE = 0.5                                 # Determine whether to round up or down
TIMECODE_IN_FRAMES = "00:{0:02d}:{1:02d}:{2:02d}"   # Timecode in frames
TIMECODE_IN_MS = "00:{0:02d}:{1:02d},{2:03d}"       # Timecode in milliseconds

class Timecode:
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0, frames: int = 0, frame_rate: float = 24.0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames
        self.frame_rate = frame_rate

    def __init__(self, x: int, frame_rate: float = 24.0):
        if isinstance(x, int):
            total_frames = x
            self.frame_rate = frame_rate
            self.hours = int(total_frames // (60 * 60 * frame_rate))
            total_frames -= int(self.hours * 60 * 60 * frame_rate)
            self.minutes = int(total_frames // (60 * frame_rate))
            total_frames -= int(self.minutes * 60 * frame_rate)
            self.seconds = int(total_frames // frame_rate)
            self.frames = int(total_frames % frame_rate)
        else:
            self.hours, self.minutes, self.seconds, self.frames = map(int, x.split(":"))
            self.frame_rate = frame_rate

    def get_total_frames(self) -> int:
        total_seconds = self.minutes * 60 + self.seconds
        return total_seconds * self.frame_rate + self.frames

    def get_timecode_in_frames(self) -> str:
        return TIMECODE_IN_FRAMES.format(self.minutes, self.seconds, self.frames)

    def get_timecode_in_ms(self) -> str:
        ms = int((self.frames * 1000) / self.frame_rate + ROUNDING_RATE)
        return TIMECODE_IN_MS.format(self.minutes, self.seconds, ms)
    
    def __eq__(self, other):
        if isinstance(other, Timecode):
            return (self.hours == other.hours and
                    self.minutes == other.minutes and
                    self.seconds == other.seconds and
                    self.frames == other.frames and
                    self.frame_rate == other.frame_rate)
        
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, Timecode):
            return self.get_total_frames() < other.get_total_frames()
        
        return False

    def __le__(self, other):    
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):    
        return not self.__le__(other)

    def __ge__(self, other):    
        return not self.__lt__(other)
    
    def __add__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() + other.get_total_frames()
            return Timecode(frames=total_frames, frame_rate=self.frame_rate)
        
        return None

    def __sub__(self, other):
        if isinstance(other, Timecode):
            total_frames = self.get_total_frames() - other.get_total_frames()
            return Timecode(frames=total_frames, frame_rate=self.frame_rate)
        
        return None