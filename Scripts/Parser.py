from enum import Enum
from docx import Document

from Scripts.Script import Script
from Scripts.Loop import Loop

SHOULD_BE_UPPER = True

# Indices
COLUMN_NAMES_ROW = 0
STARTING_ROW = 1

# Error messages
COLUMN_HEADER_NOT_FOUND = "Unable to resolve this LDS Script format. {0} column not found."
NO_TIMECODE_FOUND = "No timecodes found in script"
SCRIPT_TABLE_NOT_FOUND = "Unable to resolve this LDS Script format. No script table found."
INVALID_COLUMN_INDEX = "Invalid column index: {0}"

# Column headers
class ColumnNames(Enum):
    ID = "LOOP"
    TIMECODE = "TIMECODE"
    CHARACTER = "CHARACTER"
    ENGLISH = "ENGLISH"
    TRANSLATION = "TRANSLATION"

REQUIRED_COLUMNS = [ColumnNames.ID, ColumnNames.CHARACTER, ColumnNames.ENGLISH,
                    ColumnNames.TRANSLATION]

class Parser:
    def __init__(self):
        self.script: Script = Script()
        self.header_to_index = {}


    def parse_script(self, filename: str) -> Script:
        self.document = Document(filename)

        self.assign_translation_table()
        self.assign_headers()
        self.parse_translation_table()

        return self.script


    def assign_translation_table(self) -> None:
        self.translation_table = self.find_translation_table()
        assert self.translation_table is not None, SCRIPT_TABLE_NOT_FOUND

    
    def assign_headers(self) -> None:
        self.generate_header_dictionary()
        self.validate_columns()


    def parse_translation_table(self) -> None:
        rows = self.translation_table.rows[STARTING_ROW:]
        for row in rows:
            self.add_row_to_script(row)


    def add_row_to_script(self, row: list) -> None:
        loop = self.create_loop_from_row(row)
        self.script.add_loop_to_script(loop)


    def does_column_exist(self, column_name: ColumnNames):
        return column_name.value in self.header_to_index.keys()
    
    
    def validate_columns(self):       
        for column in REQUIRED_COLUMNS:
            assert self.does_column_exist(column), \
                COLUMN_HEADER_NOT_FOUND.format(column)


    def generate_header_dictionary(self) -> None:
        header_row = self.translation_table.rows[COLUMN_NAMES_ROW]
        
        for i in range(len(header_row.cells)):
            self.add_header_from_cell(header_row, i)
    

    def add_header_from_cell(self, header_row: str, index: int) -> None:
        cell = header_row.cells[index]
        header = self.get_text_from_cell(cell, SHOULD_BE_UPPER)
        self.header_to_index[header] = index


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
    

    def get_text_from_row(self, row: list, column) -> str:
        if isinstance(column, ColumnNames):
            column = self.header_to_index[column.value]
        else:
            assert isinstance(column, int), INVALID_COLUMN_INDEX.format(column)
            
        return self.get_text_from_cell(row.cells[column])
    

    def create_loop_from_row(self, row: list):
        id = self.get_text_from_row(row, ColumnNames.ID)
        character = self.get_text_from_row(row, ColumnNames.CHARACTER)
        english = self.get_text_from_row(row, ColumnNames.ENGLISH)
        translation = self.get_text_from_row(row, ColumnNames.TRANSLATION)

        return Loop(id, character, english, translation)


    def get_text_from_cell(self, cell, is_upper: bool = False) -> str:
        """Extracts the text from a cell and returns it as a string"""

        text = cell.text.strip()
        if is_upper: text = text.upper()
        
        return text


    def split_row(self, row: list, is_upper: bool = False) -> list:
        """Extracts the text from a row and returns it as a list of strings"""
        split_row = [self.get_text_from_cell(cell, is_upper) for cell in row.cells]
        return split_row


    def find_translation_table(self):
        for table in self.document.tables:
            if self.does_table_contain_script(table):
                return table

        return None
    
    
    def does_table_contain_script(self, table) -> bool:
        header_row = table.rows[COLUMN_NAMES_ROW]
        header_text = self.split_row(header_row, SHOULD_BE_UPPER)

        return ColumnNames.CHARACTER.value in header_text

