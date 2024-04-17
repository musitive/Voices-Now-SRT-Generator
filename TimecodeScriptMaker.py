from FileMaker import FileMaker
from ProToolsMarkerManager import ProToolsMarkerManager
from ScriptManager import LdsScriptManager

class TimecodeScriptMaker(FileMaker):
    def __init__(self, timecode_filename: str, script_filename: str):
        self.marker_manager = ProToolsMarkerManager(timecode_filename)          # Open Pro Tools Marker file
        self.script_manager = LdsScriptManager(script_filename)                 # Open Word Document


    def enhance_script(self, new_filename: str) -> None:
        # Initial formatting
        self.script_manager.script.set_styles()
        self.script_manager.script.change_orientation()
        self.script_manager.script.initialize_tables()

        # Inner function to update the file
        def update_file(self, marker, next_marker):
            self.script_manager.add_row_to_new_table(marker.timecode, next_marker.timecode)

        # Read through markers
        self.read_through_markers(update_file)

        # Final formatting
        self.script_manager.script.prevent_document_break()
        self.script_manager.script.remove_table(0)

        # Save the new file
        self.script_manager.script.save_as_new_script(new_filename)

        return
        