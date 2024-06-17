import csv

LDS_LANGUAGES_CSV = "Captions/All_Languages.csv"

LANG_ID = 0
LANG_CODE = 1
LANG_NAME = 2
LANG_SCRIPT = 3
LANG_SPLITTER = 4
LANG_MAX_LINE_COUNT = 5

# ================================================================================================

class LanguageManager:
    class LanguageInfo:
        def __init__(self, lang_code: str, lang_name: str, lang_script: str, lang_splitter: bool, lang_max_line_count: int):
            self.code = lang_code
            self.name = lang_name
            self.script = lang_script
            self.splitter = lang_splitter
            self.max_line_count = lang_max_line_count

    # --------------------------------------------------------------------------------
    # LanguageManager
    def __init__(self) -> None:
        with open(LDS_LANGUAGES_CSV, 'r') as file:
            # Generate a dictionary of language codes to languages
            reader = csv.reader(file)
            self.lang_info = {}
            self.lang_to_code = {}

            for row in reader:
                self.lang_info[row[LANG_CODE].upper()] = LanguageManager.LanguageInfo(row[LANG_CODE].upper(), row[LANG_NAME], row[LANG_SCRIPT], bool(row[LANG_SPLITTER]), int(row[LANG_MAX_LINE_COUNT]))
                self.lang_to_code[row[LANG_NAME]] = row[LANG_CODE].upper()
            
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get the language from the language code
    # code: str       - the language code
    ## returns: str   - the language
    def get_lang(self, code: str) -> str:
        return self.lang_info[code.upper()].name
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get the language code from the language
    # lang: str       - the language
    ## returns: str   - the language code
    def get_code(self, lang: str) -> str:
        return self.lang_to_code[lang]
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get the script type from the language code
    # code: str       - the language code
    ## returns: str   - the script type
    def get_script(self, code: str) -> str:
        return self.lang_info[code.upper()].script
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get the splitter support from the language code
    # code: str       - the language code
    ## returns: str   - the splitter support
    def get_splitter(self, code: str) -> bool:
        return self.lang_info[code.upper()].splitter
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get max line count from the language code
    # code: str       - the language code
    ## returns: int   - the max line count
    def get_max_line_count(self, code: str) -> int:
        return self.lang_info[code.upper()].max_line_count
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get language info from the language code
    # code: str       - the language code
    ## returns: list  - the language info
    def get_lang_info(self, code: str) -> list:
        return [self.lang_info[code.upper()].id, self.lang_info[code.upper()].code, self.lang_info[code.upper()].name, self.lang_info[code.upper()].script, self.lang_info[code.upper()].splitter, self.lang_info[code.upper()].max_line_count]
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Add a column to the language CSV
    @staticmethod
    def add_column(empty_cell: str):
        with open(LDS_LANGUAGES_CSV, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]

        for row in data:
            row.append(empty_cell)

        with open(LDS_LANGUAGES_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    # --------------------------------------------------------------------------------

# ================================================================================================