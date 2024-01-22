from docx import Document

class LdsScript:

    def __init__(self, wordFilename: str):
        self.document = Document(wordFilename)

        # Python-docx set-up
        # Most LDS Translations should be in the second table, fourth column
        self.tables = self.document.tables
        self.columns = self.tables[1].columns
        if len(self.columns) == 4:
            self.translation = self.columns[3]
        elif len(self.columns) == 5:
            self.translation = self.columns[4]
        else:
            raise Exception("Unable to resolve this LDS Script format.")
        self.newSection = True

    def get_translation(self, translationRow: int) -> str:
        return self.translation.cells[translationRow].text