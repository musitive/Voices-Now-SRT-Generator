from docx import Document

# ================================================================================================

class Script:
    pass

# ================================================================================================

LDS_LOOP_ID = "LOOP"
LDS_TIMECODE_ID = "TIMECODE"
LDS_CHARACTER_ID = "CHARACTER"
LDS_DIAL_ID = "ENGLISH"
LDS_TRANSLATION_ID = "TRANSLATION"

class LdsScript(Script):
    # ----------------------------------------------------------------------------
    class ScriptBlock:
        def __init__(self, loop: str, character: str, english: str, translation: str):
            self.loop = loop
            self.character = character
            self.english = english
            self.translation = translation
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # LdsScript
    # wordFilename: str    - the name of the file containing the script data
    def __init__(self, wordFilename: str):
        self.document = Document(wordFilename)

        self.headers = {}

        # Find the correct table
        for table in self.document.tables:
            if LDS_CHARACTER_ID in [cell.text.strip().upper() for cell in table.rows[0].cells]:
                self.translation_table = table
                break
        
        header_row = self.translation_table.rows[0]
        for i in range(len(header_row.cells)):
            self.headers[header_row.cells[i].text.upper().strip()] = i

        if (LDS_LOOP_ID not in self.headers or
            LDS_CHARACTER_ID not in self.headers or
            LDS_DIAL_ID not in self.headers or
            LDS_TRANSLATION_ID not in self.headers):
            raise Exception("Unable to resolve this LDS Script format.")
        
        get_text_from_row = lambda cells: (cells[self.headers[LDS_LOOP_ID]].text.replace("\n", "").strip(),
                                           LdsScript.ScriptBlock(cells[self.headers[LDS_LOOP_ID]].text.replace("\n", "").strip(),
                                                                cells[self.headers[LDS_CHARACTER_ID]].text.replace("\n", "").strip(),
                                                                cells[self.headers[LDS_DIAL_ID]].text.replace("\n", "").strip(),
                                                                cells[self.headers[LDS_TRANSLATION_ID]].text.replace("\n", "").strip()))
        self.blocks = dict([get_text_from_row(row.cells) for row in self.translation_table.rows[1:]])
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Get the translation of a specific row in the script
    # translationRow  - The row number of the translation to get
    def get_translation(self, translationRow: str) -> str:
        return self.blocks[translationRow].translation
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Check if the script has timecodes
    def has_timecodes(self) -> bool:
        return LDS_TIMECODE_ID in self.headers
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Get the script timecodes
    def get_timecodes(self) -> dict:
        assert self.has_timecodes(), "No timecodes found in script"

        return dict([(row.cells[self.headers[LDS_LOOP_ID]].text.strip(),
                        row.cells[self.headers[LDS_TIMECODE_ID]].text.strip()) for row in self.translation_table.rows[1:]])
    # ----------------------------------------------------------------------------

# ================================================================================================