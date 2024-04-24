from Scripts.Script import LdsScript

class ScriptManager:
    pass

class LdsScriptManager(ScriptManager):
    def __init__(self, filename: str):
        self.script = LdsScript(filename)


    """
    Iterate to the next translation in the script
    """
    def get_translation(self, loop_name: str) -> str:
        translation = self.script.get_translation(loop_name)
        return translation