"""
Code to extract Pro Tools Markers
Author: Dallin Frank

Run test cases:
py -m unittest TestProToolsMarkerManager
"""

from ProToolsMarkers.ProToolsMarker import ProToolsMarker
import re

PT_MARKER_DATA_START = 12
PT_FRAMERATE_INDEX = 4

PT_MARKER_ID = "#"
PT_LOCATION_ID = "LOCATION"
PT_TIMEREF_ID = "TIME REFERENCE"
PT_UNITS_ID = "UNITS"
PT_NAME_ID = "NAME"
PT_TNAME_ID = "TRACK NAME"
PT_TTYPE_ID = "TRACK TYPE"
PT_COMMENTS_ID = "COMMENTS"

class ProToolsMarkerManager:
    def __init__(self, filename: str):
        with open(filename, 'r') as timecode_file:
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

                elif timecode_index == PT_MARKER_DATA_START:
                    header_data = re.split(r"\t", line)
                    self.column_headers = {header_data[i] : i for i in range(len(header_data))}
                    continue

                # Split the marker data and timestamp
                self.add_new_marker(line)

                # Update iterators
                timecode_index += 1

    # Refactor this code

    """
    Add a new marker to the list of markers
    line: str       - the line of text containing the marker data
    """
    def add_new_marker(self, line: str) -> None:
        marker_data = re.split(r"\t", line)
        marker_data = [x.strip() for x in marker_data]

        marker_id = marker_data[self.column_headers[PT_MARKER_ID]]
        location = marker_data[self.column_headers[PT_LOCATION_ID]]
        time_reference = marker_data[self.column_headers[PT_TIMEREF_ID]]
        units = marker_data[self.column_headers[PT_UNITS_ID]]
        name = marker_data[self.column_headers[PT_NAME_ID]]
        comments = marker_data[self.column_headers[PT_COMMENTS_ID]]

        self.markers.append(ProToolsMarker(marker_id, location, time_reference, units, name, comments))


    """
    Get the next marker using iterator behavior
    """
    def get_next_marker(self) -> ProToolsMarker:
        if self.current_marker_index >= len(self.markers):
            return None

        marker = self.markers[self.current_marker_index]
        self.current_marker_index += 1

        return marker

    """
    Get a marker by index
    index: int      - the index of the marker
    """
    def get_marker(self, index: int) -> ProToolsMarker:
        assert index >= 0 and index < len(self.markers), f"The Pro Tools Marker index {index} is out of bounds"        
        return self.markers[index]
    