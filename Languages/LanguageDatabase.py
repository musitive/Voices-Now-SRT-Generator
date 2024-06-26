import csv
from enum import IntEnum

# Paths
LDS_LANGUAGES_CSV = "Captions/All_Languages.csv"

# Errors
INVALID_CODE_LENGTH = "Error: Language code {0} must be 3 characters"
INVALID_CODE_FORMAT = "Error: Language code {0} must be uppercase"
INVALID_CHAR_COUNT = "Error: Max character count {0} must be greater than 0"

def add_column(empty_cell: str) -> None:
    """Add a column to the LDS_LANGUAGES_CSV file with the specified empty
        cell value. ADD VALUE TO THE ENUM"""
    # TODO: Add value to the enum
    with open(LDS_LANGUAGES_CSV, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    for row in data:
        row.append(empty_cell)

    with open(LDS_LANGUAGES_CSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

class ColumnHeaders(IntEnum):
    ID = 0
    CODE = 1
    NAME = 2
    SCRIPT_TYPE = 3
    SUPPORTS_SPLIT = 4
    MAX_CHAR_COUNT = 5

def validate_language_code(code: str) -> None:
    """Validate the language code"""
    # assert len(code) == 3, INVALID_CODE_LENGTH.format(code)
    assert code.isupper(), INVALID_CODE_FORMAT.format(code)

class LanguageDatabase:
    class Language:
        def __init__(self, id: str, code: str, name: str, script_type: str,
                     supports_split: bool, max_char_count: int):
            """Language subclass to store language information"""
            
            validate_language_code(code)
            assert max_char_count > 0, INVALID_CHAR_COUNT.format(max_char_count)

            self.id = id
            self.code = code
            self.name = name
            self.script_type = script_type
            self.supports_split = supports_split
            self.max_char_count = max_char_count


    def __init__(self, csv_filename: str = LDS_LANGUAGES_CSV):
        """Initialize the language database from a CSV file"""
        with open(csv_filename, 'r') as file:

            reader = csv.reader(file)
            self.code_to_language: dict[str, LanguageDatabase.Language] = {}
            self.name_to_code: dict[str, str] = {}

            for row in reader:
                self.add_language_from_row(row)


    def add_language_from_row(self, row: list[str]) -> None:
        """Add a language to the language database from a row of data"""

        id = row[ColumnHeaders.ID]
        code = row[ColumnHeaders.CODE].upper()
        name = row[ColumnHeaders.NAME]
        script_type = row[ColumnHeaders.SCRIPT_TYPE]
        supports_split = bool(row[ColumnHeaders.SUPPORTS_SPLIT])
        max_char_count = int(row[ColumnHeaders.MAX_CHAR_COUNT])

        language = LanguageDatabase.Language(id, code, name, script_type,
                                             supports_split, max_char_count)

        self.code_to_language[code] = language
        self.name_to_code[name] = code


    def get_name(self, code: str) -> str:
        validate_language_code(code)
        return self.code_to_language[code].name


    def get_code(self, name: str) -> str:
        return self.name_to_code[name]


    def get_script_type(self, code: str) -> str:
        validate_language_code(code)
        return self.code_to_language[code].script_type


    def language_supports_split(self, code: str) -> bool:
        validate_language_code(code)
        return self.code_to_language[code].supports_split


    def get_max_char_count(self, code: str) -> int:
        validate_language_code(code)
        return self.code_to_language[code].max_char_count


    def get_language(self, code: str) -> Language:
        return self.code_to_language[code]