from Scripts.Script import LdsScript

# ================================================================================================

class ScriptManager:
    pass

# ================================================================================================

class LdsScriptManager(ScriptManager):
    # ----------------------------------------------------------------------------
    def __init__(self, filename: str):
        self.script = LdsScript(filename)
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Iterate to the next translation in the script
    def get_translation(self, loop_name: str) -> str:
        translation = self.script.get_translation(loop_name)
        return translation
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Check if the script has timecodes
    def has_timecodes(self) -> bool:
        return self.script.has_timecodes()
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # Get the script timecodes
    def get_timecodes(self) -> dict:
        return self.script.get_timecodes()
    # ----------------------------------------------------------------------------

# ================================================================================================