"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import PySimpleGUI as sg
from Captions.CaptionMaker import SRTMaker

# =================================================================================================

# String constants
STRING001 = "Choose LDS Translation: "
STRING002 = "Choose Timecode File: "
STRING003 = "Choose Destination Folder: "
STRING004 = "Choose SRT File Name: "
STRING005 = "Confirm"
STRING006 = "Please enter a value in all fields"
STRING007 = "File not found"
STRING008 = "Something went wrong :/"
STRING009 = "Voices Now SRT Generator"
STRING010 = ".srt"

# =================================================================================================

def main() -> None:
    # Create the layout
    layout = [  [sg.T("")], \
                [sg.Text(STRING001)], \
                [sg.Input(), sg.FileBrowse(key="trans")], \
                [sg.T("")], \
                [sg.Text(STRING002)], \
                [sg.Input(), sg.FileBrowse(key="time")], \
                [sg.T("")], \
                [sg.Text(STRING003)], \
                [sg.Input(), sg.FolderBrowse(key="dest")], \
                [sg.T("")], \
                [sg.Text(STRING004)], \
                [sg.Input(key="filename"), sg.Text(STRING010)], \
                [sg.T("")], \
                [sg.Button(STRING005)]]

    # Create the window
    window = sg.Window(STRING009, layout, size=(500,500))

    # Event loop
    while True:
        event, values = window.read()

        # End program if user closes window or presses the OK button
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == "Submit":
            trans = values["trans"]
            time = values["time"]
            dest = values["dest"]
            filename = values["filename"]

            if trans == "" or time == "" or dest == "" or filename == "":
                sg.popup_ok(STRING006)
                continue
            else:
                try:
                    # TODO: Add language selection dropdown
                    srt_maker = SRTMaker(trans, time, f"{dest}/{filename}.srt", filename[:-3])
                    # TODO: Add split option checkbox
                    srt_maker.create_captions(True)
                except FileNotFoundError:
                    sg.popup_error_with_traceback(STRING007)
                except Exception as e:
                    sg.popup_error_with_traceback(STRING008)
                    print(str(e))
            break

    window.close()
    
# =================================================================================================

if __name__ == "__main__":
    main()