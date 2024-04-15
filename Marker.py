from Timecode import Timecode

class Marker:

    def __init__(self, marker_id: str, location: str, time_reference: str,
                 units: str, name: str, frame_rate: float):
        self.marker_id = marker_id
        self.time_reference = time_reference
        self.units = units
        self.name = name
        self.frame_rate = frame_rate
        self.timecode = Timecode(location, frame_rate)
    
    def __eq__(self, other):
        if isinstance(other, Marker):
            return (self.marker_id == other.marker_id and
                    self.minutes == other.minutes and
                    self.seconds == other.seconds and
                    self.frames == other.frames and
                    self.time_reference == other.time_reference and
                    self.units == other.units and
                    self.name == other.name and
                    self.frame_rate == other.frame_rate)
        
        return False