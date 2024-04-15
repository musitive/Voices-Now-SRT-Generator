from Script import LdsScript

class ScriptManager:
    pass

class LdsScriptManager(ScriptManager):
    def __init__(self, filename: str):
        self.script = LdsScript(filename)
        self.translation_index = 1

    def get_script(self):
        return self.script

    def get_next_translation(self):
        translation = self.script.get_translation(self.translation_index)
        self.translation_index += 1

        return translation

    def get_translation(self, index: int):
        return self.script.get_translation(index)

    def get_character(self, index: int):
        return self.script.get_character(index)

    def get_loops(self, index: int):
        return self.script.get_loops(index)

    def get_characters(self):
        return self.script.get_characters()

    def get_loops(self):
        return self.script.get_loops