from docx import Document

# Column headers
LOOP = "LOOP"
TIMECODE = "TIMECODE"
CHARACTER = "CHARACTER"
ENGLISH = "ENGLISH"
TRANSLATION = "TRANSLATION"

def get_text(cells: list, column: int) -> str:
    return cells[column].text.replace("\n", "").strip()

class Script:
    def __init__(self, wordFilename: str):
        """Constructor for the Script class
        
        Keyword arguments:
        """
        self.document = Document(wordFilename)

        self.headers = {}

        # Find the correct table
        for table in self.document.tables:
            if CHARACTER in [cell.text.strip().upper() for cell in table.rows[0].cells]:
                self.translation_table = table
                break
        
        # Create a dictionary of column headers
        header_row = self.translation_table.rows[0]
        for i in range(len(header_row.cells)):
            self.headers[header_row.cells[i].text.upper().strip()] = i

        # Check for required fields
        assert LOOP in self.headers, "Unable to resolve this LDS Script format. LOOP column not found."
        assert CHARACTER in self.headers, "Unable to resolve this LDS Script format. TIMECODE column not found."
        assert ENGLISH in self.headers, "Unable to resolve this LDS Script format. TIMECODE column not found."
        assert TRANSLATION in self.headers, "Unable to resolve this LDS Script format. TRANSLATION column not found."
        
        # Create a dictionary of script blocks
        STARTING_ROW = 1

        rows = self.translation_table.rows[STARTING_ROW:]
        self.blocks = dict([Script.Loop.from_row(row) for row in rows])

    
    @classmethod
    def from_file(cls, wordFilename: str):
        return cls(wordFilename)


    def get_translation(self, translationRow: str) -> str:
        return self.blocks[translationRow].translation


    def has_timecodes(self) -> bool:
        return TIMECODE in self.headers


    def get_timecodes(self) -> dict:
        assert self.has_timecodes(), "No timecodes found in script"

        timecodes = {}

        for row in self.translation_table.rows[1:]:
            loop = get_text(row.cells, LOOP)
            timecodes[loop] = get_text(row.cells, TIMECODE)

        return timecodes
    

    class Loop:
        def __init__(self, id: str, character: str, english: str, translation: str):
            self.id = id
            self.character = character
            self.english = english
            self.translation = translation
        
        @classmethod
        def from_row(cls, row: list):
            cells = row.cells

            loop_id = get_text(cells, LOOP)
            character = get_text(cells, CHARACTER)
            dial = get_text(cells, ENGLISH)
            translation = get_text(cells, TRANSLATION)
            
            return cls(loop_id, character, dial, translation)