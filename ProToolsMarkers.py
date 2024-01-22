"""
Code to extract Pro Tools Markers
Author: Dallin Frank

Run test cases:
py -m unittest TestProToolsMarkers
"""

from Marker import Marker
import re

class ProToolsMarkers:
    markers = []

    def __init__(self, filename: str):
        timecode_file = open(filename, "r")
        timecode_index = 0
        self.markers = []

        # Iterate through the timecode file
        for line in timecode_file:
            
            # Extract the framerate from the file
            if timecode_index == 4:
                _, frame_rate = re.split(r"\t", line)
                frame_rate, _ = re.split("\s", frame_rate, 1)
                self.FRAME_RATE = float(frame_rate)

                timecode_index += 1
                continue

            # Currently useless metadata from Pro Tools, skip it
            elif timecode_index < 12:
                timecode_index += 1
                continue

            # Split the marker data and timestamp
            marker_id, location, time_reference, units, name, _ = re.split("\s+", line)
            self.markers.append(Marker(marker_id, location, time_reference, units, name, self.FRAME_RATE))

            # Update iterators
            timecode_index += 1

        timecode_file.close()

    def get_marker(self, index: int) -> Marker:
        if index < 0 or index >= len(self.markers):
            raise Exception("The Pro Tools Marker index {0} is out of bounds. Make sure that the number of named markers matches the number of loops.")
        
        return self.markers[index]
        
    def get_markers(self):
        return self.markers