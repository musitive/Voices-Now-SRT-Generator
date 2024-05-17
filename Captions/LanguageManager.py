import csv

LDS_LANGUAGES_CSV = "Captions/All_Languages.csv"

# ================================================================================================

class LanguageManager:
    # --------------------------------------------------------------------------------
    # LanguageManager
    def __init__(self) -> None:
        with open(LDS_LANGUAGES_CSV, 'r') as file:
            # Generate a dictionary of language codes to languages
            reader = csv.reader(file)
            self.code_to_lang = {lang[1].upper(): lang[2] for lang in reader}

            # Generate a dictionary of languages to language codes
            file.seek(0)
            self.lang_to_code = {lang[2]: lang[1].upper() for lang in reader}

            # Generate a dictionary of language codes to script types
            file.seek(0)
            self.code_to_script = {lang[1].upper(): lang[3] for lang in reader}

            # Generate a dictionary of language codes to splitter support
            file.seek(0)
            self.code_to_splitter = {lang[1].upper(): lang[4] for lang in reader}
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get the language from the language code
    # code: str       - the language code
    ## returns: str   - the language
    def get_lang(self, code: str) -> str:
        return self.code_to_lang[code.upper()]
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
        return self.code_to_script[code.upper()]
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Get the splitter support from the language code
    # code: str       - the language code
    ## returns: str   - the splitter support
    def get_splitter(self, code: str) -> bool:
        return bool(self.code_to_splitter[code.upper()])
    # --------------------------------------------------------------------------------

# ================================================================================================