from ProTools.Session import Session
from Scripts.Script import Script
from Scripts.Parser import Parser as ScriptParser
from Languages.Language import Language

VON_MAC = "/Volumes/VONGeneral/LDS/~Current Projects"
VON_WIN = ""

PROJECT_PATH = "/{0}/{1}/MFD_TrainingCouncil{2}.{3}"

SCRIPT_FOLDER_NAME = "Scripts"
SCRIPT_EXTENSION = "docx"

TIMECODE_FOLDER_NAME = "Timecode"
TIMECODE_EXTENSION = "txt"

class Project(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Project, cls).__new__(cls)
        return cls.instance
    

    def open_session_from_filename(self, filename: str):
        file_path = self.format_file_path(self.language.name, TIMECODE_FOLDER_NAME, filename, TIMECODE_EXTENSION)
        self.open_session(file_path)


    def open_session(self, timecode_path: str):
        self.session = Session(timecode_path)


    def open_script_from_filename(self, filename: str):
        file_path = self.format_file_path(self.language.name, SCRIPT_FOLDER_NAME, filename, SCRIPT_EXTENSION)
        self.open_script(file_path)


    def open_script(self, script_path: str):
        script_parser = ScriptParser()
        self.script = script_parser.parse_script(script_path)


    def set_project_path(self, project_path: str):
        self.project_path = project_path

    
    def set_language(self, language: Language):
        self.language = language

    
    def set_data_type(self, data_type: str):
        self.data_type = data_type

    
    def format_file_path(self, language: str, folder_name: str, filename: str, extension: str):
        return f"{VON_MAC}/{self.project_path}/{language}/{folder_name}/{filename}.{extension}"