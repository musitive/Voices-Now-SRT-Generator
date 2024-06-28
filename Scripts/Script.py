from Scripts.Loop import Loop

class Script:
    def __init__(self):
        self.loops: dict[str, Loop] = {}
    
    def add_loop_to_script(self, loop: Loop) -> None:
        self.loops[loop.id] = loop

    def has_timecodes(self) -> bool:
        return False
    
    def get_translation(self, loop_id: int) -> str:
        return self.loops[loop_id].translation