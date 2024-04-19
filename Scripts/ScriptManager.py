import Script
from importlib import reload

reload(Script)

from Script import LdsScript

class ScriptManager:
    pass

class LdsScriptManager(ScriptManager):
    def __init__(self, filename: str):
        self.script = LdsScript(filename)
        self.translation_index = 0


    """
    Iterate to the next translation in the script
    """
    def get_next_translation(self) -> str:
        translation = self.script.get_translation(self.translation_index)
        self.translation_index += 1
        return translation