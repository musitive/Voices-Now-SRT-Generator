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

# ================================================================================================

class LdsScript(Script):
    # ----------------------------------------------------------------------------
    class ScriptBlock:
        # ------------------------------------------------------------------------
        # ScriptBlock
        # loop: str         - the loop number of the block
        # character: str    - the character speaking in the block
        # english: str      - the english text of the block
        # translation: str  - the translation of the block
        def __init__(self, loop: str, character: str, english: str, translation: str):
            self.loop = loop
            self.character = character
            self.english = english
            self.translation = translation
        # ------------------------------------------------------------------------
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
        
        # Create a dictionary of column headers
        header_row = self.translation_table.rows[0]
        for i in range(len(header_row.cells)):
            self.headers[header_row.cells[i].text.upper().strip()] = i

        # Check for required fields
        assert LDS_LOOP_ID in self.headers, "Unable to resolve this LDS Script format. LOOP column not found."
        assert LDS_CHARACTER_ID in self.headers, "Unable to resolve this LDS Script format. TIMECODE column not found."
        assert LDS_DIAL_ID in self.headers, "Unable to resolve this LDS Script format. TIMECODE column not found."
        assert LDS_TRANSLATION_ID in self.headers, "Unable to resolve this LDS Script format. TRANSLATION column not found."

        # Inner function to get the text from a row
        def get_text_from_row(cells: list, id: str):
            # Get the text from the row
            loop = self.get_text(cells, LDS_LOOP_ID)
            character = self.get_text(cells, LDS_CHARACTER_ID)
            dial = self.get_text(cells, LDS_DIAL_ID)
            translation = self.get_text(cells, LDS_TRANSLATION_ID)
            
            script_block = LdsScript.ScriptBlock(loop, character, dial, translation)

            return loop, script_block
        
        # Create a dictionary of script blocks
        self.blocks = dict([get_text_from_row(row.cells) for row in self.translation_table.rows[1:]])
    # ----------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Get the text from a specific cell in a row
    # cells  - The cells in the row
    # id     - The ID of the cell to get the text from
    ## returns: str
    def get_text(self, cells: list, id: str) -> str:
        return cells[self.headers[id]].text.replace("\n", "").strip()
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

        return dict([(self.get_text(row.cells, LDS_LOOP_ID),
                      self.get_text(row.cells, LDS_TIMECODE_ID)) for row in self.translation_table.rows[1:]])
    # ----------------------------------------------------------------------------

# ================================================================================================