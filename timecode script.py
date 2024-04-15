from ProToolsMarkerManager import ProToolsMarkers
from Script import LdsScript

def enhance_script(filename: str, timecode_filename: str, new_filename: str) -> None:
    script = LdsScript(filename)
    markers = ProToolsMarkers(timecode_filename)

    script.set_styles()
    script.change_orientation()
    script.initialize_tables()

    timecode_index = 0
    translation_index = 1

    marker = markers.get_marker(timecode_index)
    in_time = marker.get_timecode_in_frames()
    n = len(markers.get_markers())

    def update_indices():
        nonlocal marker, next_marker, in_time, out_time, timecode_index
        timecode_index += 1
        marker = next_marker
        in_time = out_time


    for timecode_index in range(n):
        next_marker = markers.get_marker(timecode_index+1)
        if next_marker == None:
            break
        out_time = next_marker.get_timecode_in_frames()

        name = marker.get_name()
        if name == 'x' or name == 'END':
            update_indices()
            continue

        script.add_row_to_new_table(translation_index, in_time, out_time)

        update_indices()
        translation_index += 1


    script.prevent_document_break()
    script.remove_table(0)

    script.save_as_new_script(new_filename)

# Test Case
if __name__ == '__main__':
    enhance_script("tests/test.docx", "tests/BMVL_308_Timecode.txt", "tests/output.docx")
    enhance_script("tests/BMVL_501_PD80000808_SCR_IND-INDONESIAN.docx", "tests/BMVL_501_timecode.txt", "tests/output3.docx")