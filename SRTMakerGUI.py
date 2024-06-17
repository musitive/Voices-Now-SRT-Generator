"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import re
import PySimpleGUI as sg
from Captions.CaptionMaker import CaptionMaker
from Captions.LanguageManager import LanguageManager
from ProToolsData.Timecode import Timecode

# =================================================================================================

# String constants
STRING001 = "Choose Script: "
STRING002 = "Choose Timecode File: "
STRING003 = "Choose Destination Folder: "
STRING004 = "Choose SRT File Name: "
STRING005 = "Confirm"
STRING006 = "Please enter a value in all fields"
STRING007 = "File not found"
STRING008 = "Something went wrong :/"
STRING009 = "Voices Now SRT Generator"
STRING010 = ".srt"
STRING011 = "Select Language: "

CAPTION_SPLITTER_NAME = "CaptionSplitter"
TIMECODE_SCRIPT_GENERATOR_NAME = "Timecode Script Generator"
ADR_CHART_GENERATOR_NAME = "ADR Chart Generator"

# =================================================================================================

# ------------------------------------------------------------------------------
# Program Select
## returns: str - the name of the program to run
def program_select() -> str:
    PROGRAM_SELECT_RADIO_KEY = "PROGRAM"
    selected_program = None

    layout = [  [sg.Text('Which program would you like to run?')],
                [sg.Radio(CAPTION_SPLITTER_NAME, PROGRAM_SELECT_RADIO_KEY, default=True)],
                [sg.Radio(TIMECODE_SCRIPT_GENERATOR_NAME, PROGRAM_SELECT_RADIO_KEY, default=False)],
                [sg.Radio(ADR_CHART_GENERATOR_NAME, PROGRAM_SELECT_RADIO_KEY, default=False)],
                [sg.Button('Next')] ]

    window = sg.Window('Program Selection', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == 'Next':
            if values[0]:
                selected_program = CAPTION_SPLITTER_NAME
            elif values[1]:
                selected_program = TIMECODE_SCRIPT_GENERATOR_NAME
            elif values[2]:
                selected_program = ADR_CHART_GENERATOR_NAME
            break

    window.close()

    return selected_program
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Caption Splitter
## returns: None
def caption_splitter() -> None:
    lang_manager = LanguageManager()
    languages = list(lang_manager.lang_to_code.keys())
    
    lang_code = "ENG"
    split = True

    # GET LANGUAGE AND SPLIT OPTIONS
    layout = [  [sg.Text(STRING011)],
                [sg.Combo(languages, key="lang", enable_events=True, readonly=True, default_value="English"),
                 sg.Checkbox("Split Captions?", key="split", default=True, disabled=False)],
                [sg.Text(STRING001)],
                [sg.Input(), sg.FileBrowse(key="trans")],
                [sg.Text(STRING002)],
                [sg.Input(), sg.FileBrowse(key="timecode"), sg.Combo(['EDL', 'MRK'], key="data_type", readonly=True, default_value="EDL")],
                [sg.Button('Next')]]

    window = sg.Window(CAPTION_SPLITTER_NAME, layout)

    # Event loop
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == 'lang':
            lang_code = lang_manager.get_code(values['lang'])
            split = lang_manager.get_splitter(lang_code)
            # TODO: Update the split checkbox
        if event == 'Next':
            break

    script_name = values['trans']
    max_line_count = lang_manager.get_max_line_count(lang_code)
    timecode_name = values['timecode']
    srt_name = re.sub(r'.docx', r'.srt', script_name)
    data_type = values['data_type']

    window.close()

    # REMAINING OPTIONS
    layout = [  [sg.Text("Timecode Offset (HH:MM:SS:FF): "), sg.InputText(key="offset", default_text="00:00:00:00"), sg.Combo(['adv', 'dly'], key="offset_type", readonly=True, default_value="adv")],
                [sg.Text("Max Line Count: "), sg.InputText(key="max_line_count", default_text=max_line_count)],
                [sg.Text("SRT ID Offset: "), sg.InputText(key="srt_id_offset", default_text="0")],
                [sg.Button('Generate')]]
    
    window = sg.Window(CAPTION_SPLITTER_NAME, layout)

    # Event loop
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == 'Generate':
            break
    
    time_offset = (values['offset_type'], Timecode.from_frames(values['offset']))
    max_line_count = int(values['max_line_count'])
    srt_id_offset = int(values['srt_id_offset'])

    window.close()

    # GENERATE CAPTIONS
    layout = [  [sg.Text("Generating captions...")]]
    window = sg.Window(CAPTION_SPLITTER_NAME, layout)

    window.read(timeout=0)

    caption_splitter = CaptionMaker(script_name, timecode_name, data_type, lang_code, srt_name, max_line_count, split)
    caption_splitter.create_captions(time_offset, srt_id_offset)

    window.close()

    # DONE
    layout = [  [sg.Text("Captions generated!")],
                [sg.Button('OK')]]
    window = sg.Window(CAPTION_SPLITTER_NAME, layout)
    
    # Event loop
    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'OK'):
            break
    
    window.close()

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Timecode Script Generator
## returns: None
def timecode_script_generator() -> None:
    pass
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ADR Chart Generator
## returns: None
def adr_chart_generator() -> None:
    pass
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Main
## returns: None
def main() -> None:
    # Get the program to run
    program = program_select()

    if program == CAPTION_SPLITTER_NAME:
        caption_splitter()
    elif program == TIMECODE_SCRIPT_GENERATOR_NAME:
        timecode_script_generator()
    elif program == ADR_CHART_GENERATOR_NAME:
        adr_chart_generator()
# ------------------------------------------------------------------------------

    
# =================================================================================================

if __name__ == "__main__":
    main()