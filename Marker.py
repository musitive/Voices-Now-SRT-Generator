import re

class Marker:

    ROUNDING_RATE = 0.5                 # Determine whether to round up or down

    def __init__(self, marker_id, location, time_reference, units, name, frame_rate):
        self.marker_id = marker_id
        self.location = location
        self.time_reference = time_reference
        self.units = units
        self.name = name
        self.frame_rate = frame_rate
    
    def get_timecode_in_frames(self) -> str:
        # Helper functions
        delimiter = ":"
        _, m, s, f = re.split(delimiter, self.location)
        return "00" + delimiter + m + delimiter + s + delimiter + f

    def get_timecode_in_ms(self) -> str:
        # Helper functions
        delimiter = ":"
        _, m, s, f = re.split(delimiter, self.location)
        millisec = int((int(f) * 1000) / self.frame_rate + self.ROUNDING_RATE)
        return "00" + delimiter + m + delimiter + s + "," + "%(millisec)03d" % {'millisec': millisec}
    
    def get_name(self) -> str:
        return self.name