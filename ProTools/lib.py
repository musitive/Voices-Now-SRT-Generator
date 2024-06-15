import re
from enum import Enum

ROW_DELIMITER = r"\t"

def split_row(row: str) -> list[str]:
    """Split a row of text into a list of values

    Keyword arguments:
    row: str -- the row of text to split
    """

    split_row = re.split(ROW_DELIMITER, row)
    row_values = [value.strip() for value in split_row] # Remove any leading or trailing whitespace

    return row_values

def parse_column_headers(row: str, Headers: Enum) -> dict:
    """Extract the column headers from a section of a Pro Tools session file
    
    Keyword arguments:
    row: str -- the row containing the column headers
    Headers: Enum -- the column headers
    """

    row_values = split_row(row)
    column_headers = {}

    for i in range(len(row_values)):
        value = row_values[i]
        header = Headers(value)
        column_headers[header] = i

    return column_headers