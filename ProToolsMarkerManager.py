"""
Code to extract Pro Tools Markers
Author: Dallin Frank

Run test cases:
py -m unittest TestProToolsMarkerManager
"""

from ProToolsMarker import ProToolsMarker
import re

PT_MARKER_DATA_START = 12
PT_FRAMERATE_INDEX = 4

class ProToolsMarkerManager:
    def __init__(self, filename: str):
        timecode_file = open(filename, "r")
        timecode_index = 0
        self.markers = []
        self.current_marker_index = 0

        # Iterate through the timecode file
        for line in timecode_file:
            
            # Extract the framerate from the file
            if timecode_index == PT_FRAMERATE_INDEX:
                _, frame_rate = re.split(r"\t", line)
                frame_rate, _ = re.split("\s", frame_rate, 1)
                self.FRAME_RATE = float(frame_rate)

                timecode_index += 1
                continue

            # Currently useless metadata from Pro Tools, skip it
            elif timecode_index < PT_MARKER_DATA_START:
                timecode_index += 1
                continue

            # Split the marker data and timestamp
            self.add_new_marker(line)

            # Update iterators
            timecode_index += 1

        timecode_file.close()

    # Refactor this code

    def add_new_marker(self, line: str) -> None:
        marker_data = re.split(r"\t", line)
        marker_data = [x.strip() for x in marker_data]

        if len(marker_data) == 6:
            marker_id, location, time_reference, units, name, _ = marker_data
        else:
            marker_id, location, time_reference, units, name, _, _, _ = marker_data
        self.markers.append(ProToolsMarker(marker_id, location, time_reference, units, name, self.FRAME_RATE))

    def get_next_marker(self) -> ProToolsMarker:
        if self.current_marker_index >= len(self.markers):
            return None

        marker = self.markers[self.current_marker_index]
        self.current_marker_index += 1

        return marker

    def get_marker(self, index: int) -> ProToolsMarker:
        if index < 0 or index >= len(self.markers):
            # raise Exception("The Pro Tools Marker index {0} is out of bounds. Make sure that the number of named markers matches the number of loops.".format(index))
            return None
        
        return self.markers[index]
        
    def get_markers(self):
        return self.markers
    
    def get_number_of_markers(self) -> int:
        return len(self.markers)