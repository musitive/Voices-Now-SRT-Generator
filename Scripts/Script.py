from docx import Document
from enum import Enum

COLUMN_NAMES_ROW = 0

COLUMN_HEADER_NOT_FOUND = "Unable to resolve this LDS Script format. {0} column not found."
NO_TIMECODE_FOUND = "No timecodes found in script"

# Column headers
class ColumnNames(Enum):
    ID = "LOOP"
    TIMECODE = "TIMECODE"
    CHARACTER = "CHARACTER"
    ENGLISH = "ENGLISH"
    TRANSLATION = "TRANSLATION"

REQUIRED_COLUMNS = [ColumnNames.ID, ColumnNames.CHARACTER, ColumnNames.ENGLISH,
                    ColumnNames.TRANSLATION]

def extract_text_from_cells(row: list, upper: bool = False) -> list:
    extract = lambda cell: (cell.text.strip().upper() 
                            if upper else cell.text.strip())
    
    split_row = [extract(cell) for cell in row.cells]
    return split_row

class Script:
    def __init__(self, filename: str):
        """Constructor for the Script class
        
        Keyword arguments:
        filename -- The filename of the script to be loaded
        """
        self.document = Document(filename)

        self.header_to_index = {}

        # Find the correct table
        for table in self.document.tables:
            header_row = table.rows[COLUMN_NAMES_ROW]

            if ColumnNames.CHARACTER in extract_text_from_cells(header_row, True):
                self.translation_table = table

                for i in range(len(header_row.cells)):
                    header = header_row.cells[i].text.upper().strip()
                    self.header_to_index[header] = i

                break     

        self.validate_columns()
        
        # Create a dictionary of script blocks
        STARTING_ROW = 1

        rows = self.translation_table.rows[STARTING_ROW:]
        self.blocks = dict([Script.Loop.from_row(row) for row in rows])

    def does_column_exist(self, column_name: ColumnNames):
        return column_name in self.header_to_index
    
    def validate_columns(self):       
        for column in REQUIRED_COLUMNS:
            assert self.does_column_exist(column), COLUMN_HEADER_NOT_FOUND.format(column)

    @classmethod
    def from_file(cls, wordFilename: str):
        return cls(wordFilename)


    def get_translation(self, translationRow: str) -> str:
        return self.blocks[translationRow].translation


    def has_timecodes(self) -> bool:
        return ColumnNames.TIMECODE in self.header_to_index


    def get_timecodes(self) -> dict:

        assert self.has_timecodes(), NO_TIMECODE_FOUND

        timecodes = {}

        for row in self.translation_table.rows[1:]:
            loop = self.get_text_from_row(row, ColumnNames.ID)
            timecodes[loop] = self.get_text_from_row(row, ColumnNames.TIMECODE)

        return timecodes
    
    def get_text_from_row(self, row: list, column: ColumnNames | int) -> str:
        if isinstance(column, ColumnNames):
            column = self.header_to_index[column.value]
        
        return row.cells[column].text.strip()
    
    def create_loop_from_row(self, row: list):
        id = self.get_text_from_row(row, ColumnNames.ID)
        character = self.get_text_from_row(row, ColumnNames.CHARACTER)
        english = self.get_text_from_row(row, ColumnNames.ENGLISH)
        translation = self.get_text_from_row(row, ColumnNames.TRANSLATION)

        return Script.Loop(id, character, english, translation)

    class Loop:
        def __init__(self, id: str, character: str, english: str, translation: str):
            self.id = id
            self.character = character
            self.english = english
            self.translation = translation