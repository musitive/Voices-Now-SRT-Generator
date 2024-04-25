from docx import Document

class Script:
    pass

class LdsScript(Script):
    class ScriptBlock:
        def __init__(self, loop: str, character: str, english: str, translation: str):
            self.loop = loop
            self.character = character
            self.english = english
            self.translation = translation


    def __init__(self, wordFilename: str):
        self.document = Document(wordFilename)

        self.headers = {}
        header_row = self.document.tables[1].rows[0]
        for i in range(len(header_row.cells)):
            self.headers[header_row.cells[i].text.upper().strip()] = i

        if ("LOOP" not in self.headers or
            "CHARACTER" not in self.headers or
            "ENGLISH" not in self.headers or
            "TRANSLATION" not in self.headers):
            raise Exception("Unable to resolve this LDS Script format.")
        
        get_text_from_row = lambda cells: (cells[self.headers["LOOP"]].text.replace("\n", "").strip(),
                                           LdsScript.ScriptBlock(cells[self.headers["LOOP"]].text.replace("\n", "").strip(),
                                                                cells[self.headers["CHARACTER"]].text.replace("\n", "").strip(),
                                                                cells[self.headers["ENGLISH"]].text.replace("\n", "").strip(),
                                                                cells[self.headers["TRANSLATION"]].text.replace("\n", "").strip()))
        self.blocks = dict([get_text_from_row(row.cells) for row in self.document.tables[1].rows[1:]])

    """
    Get the translation of a specific row in the script
    translationRow  - The row number of the translation to get
    """
    def get_translation(self, translationRow: str) -> str:
        return self.blocks[translationRow].translation