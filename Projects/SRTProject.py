from Projects.Project import Project

SRT_FOLDER_NAME = "Initial SRTs"
SRT_EXTENSION = "srt"

class SRTProject(Project):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SRTProject, cls).__new__(cls)
        return cls.instance
    

    def set_srt_offset(self, srt_offset):
        self.srt_offset = srt_offset


    def set_language(self, language):
        self.language = language