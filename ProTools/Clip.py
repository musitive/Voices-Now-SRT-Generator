"""
EXAMPLE CLIP

CLIP NAME                                   	Source File
Andre_01                                    	Andre_01.wav    [1]
"""

from enum import Enum

class ColumnHeaders(Enum):
    CLIP_NAME = "CLIP NAME"
    SOURCE_FILE = "Source File"

class Clip:
    def __init__(self, clip_name: str, source_file: str, channel: int = 1):
        """Constructor for the Clip class
        
        Keyword arguments:
        clip_name: str -- the name of the clip
        source_file: str -- the source file of the clip
        """

        self.clip_name = clip_name
        self.source_file = source_file
        self.channel = channel