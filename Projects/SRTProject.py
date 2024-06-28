from Projects.Project import Project
from Projects.SRTOffset import SRTOffset

SRT_FOLDER_NAME = "Initial SRTs"
SRT_EXTENSION = "srt"

class SRTProject(Project):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SRTProject, cls).__new__(cls)
        return cls.instance
    

    def set_srt_offset(self, srt_offset):
        self.srt_offset = srt_offset

    def get_srt_offset(self) -> SRTOffset:
        offset = None

        if hasattr(self, 'srt_offset'):
            offset = self.srt_offset

        return offset


    def set_language(self, language):
        self.language = language