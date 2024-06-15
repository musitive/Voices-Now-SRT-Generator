import re

ROW_DELIMITER = r"\t"

def split_row(row: str) -> list[str]:
    """Split a row of text into a list of values

    Keyword arguments:
    row: str -- the row of text to split
    """

    split_row = re.split(ROW_DELIMITER, row)
    row_values = [value.strip() for value in split_row] # Remove any leading or trailing whitespace

    return row_values