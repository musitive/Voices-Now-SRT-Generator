from Script import LdsScript

class ScriptManager:
    pass

class LdsScriptManager(ScriptManager):
    class TranslationBlock:
        def __init__(self, character: str, translation: str):
            self.character = character
            self.translation = translation

    def __init__(self, filename: str):
        self.script = LdsScript(filename)
        self.translation_index = 0
        extract_translation = lambda block: LdsScriptManager.TranslationBlock(block[0], block[1])
        self.translations = map(extract_translation, self.script.tables[1].rows[1:])

    def get_script(self):
        return self.script

    def get_next_translation(self):
        translation = self.translations[self.translation_index]
        self.translation_index += 1

        return translation

    def get_translation(self, index: int):
        return self.translations[index]

    def get_character(self, index: int):
        return self.script.get_character(index)

    def get_loops(self, index: int):
        return self.script.get_loops(index)

    def get_characters(self):
        return self.script.get_characters()

    def get_loops(self):
        return self.script.get_loops
    
    def add_row_to_new_table(self, timecode, next_timecode):
        self.script.add_row_to_new_table(self.translation_index, timecode, next_timecode)