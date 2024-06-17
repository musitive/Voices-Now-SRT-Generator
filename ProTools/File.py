"""
EXAMPLE File

Filename                                      	Location
BEEPS.1.wav                                   	Control D Internal:Users:studiod:Documents:BMVL:Season5:Tahitian:BMVL_501_TAH:Audio Files:
"""
import re
from enum import Enum

import ProTools.lib as lib

# Delimiters
ROW_DELIMITER = r"\t"

# Error Messages
INVALID_COLUMN = "Column {0} does not exist"

class ColumnHeaders(Enum):
    FILENAME = "Filename"
    LOCATION = "Location"

class File:
    def __init__(self, filename: str, location: str):
        """Constructor for the File class
        
        Keyword arguments:
        filename: str -- the name of the file
        location: str -- the location of the file
        """

        self.filename = filename
        self.location = location

    @classmethod
    def from_row(cls, header_to_index: dict, row: str):
        """Create a new Marker object from a line of Pro Tools Marker data
        
        Keyword arguments:
        column_headers: dict
        row: str -- the line of text containing the marker data
        """

        for header in header_to_index.keys():
            assert header in ColumnHeaders, INVALID_COLUMN.format(header)

        row_values = lib.split_row(row)

        get_row_value = lambda header: row_values[header_to_index[header]]

        filename = get_row_value(ColumnHeaders.FILENAME)
        location = get_row_value(ColumnHeaders.LOCATION)
        
        return cls(filename, location)