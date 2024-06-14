import re
from enum import Enum

from Marker import Marker, ColumnHeaders as MarkerHeaders
from ProTools.EDL import Clip
from Timecode import Timecode

# Delimiters
ROW_DELIMITER = r"\t"

# Indices
NAME_INDEX = 0
SAMPLE_RATE_INDEX = 1
BIT_DEPTH_INDEX = 2
SESSION_START_INDEX = 3
TIMECODE_FORMAT_INDEX = 4
NUMBER_OF_TRACKS_INDEX = 5
NUMBER_OF_CLIPS_INDEX = 6
NUMBER_OF_FILES_INDEX = 7
END_GLOBAL_DATA_INDEX = 8

class BitDepths(Enum):
    SIXTEEN = "16-bit"
    TWENTY_FOUR = "24-bit"
    THIRTY_TWO = "32-bit float"

class TimeFormats(Enum):
    BARS_BEATS = "Bars|Beats"
    MINUTES_SECONDS = "Min:Sec"
    TIMECODE = "Timecode"
    FEET_FRAMES = "Feet+Frames"
    SAMPLES = "Samples"

class SectionHeaders(Enum):
    ONLINE_FILES = "O N L I N E  F I L E S  I N  S E S S I O N"
    OFFLINE_FILES = "O F F L I N E  F I L E S  I N  S E S S I O N"
    ONLINE_CLIPS = "O N L I N E  C L I P S  I N  S E S S I O N"
    PLUG_INS_LISTING = "P L U G - I N S  L I S T I N G"
    TRACK_LISTING = "T R A C K  L I S T I N G"
    MARKERS_LISTING = "M A R K E R S  L I S T I N G"

class Session:
    def __init__(self, name: str, sample_rate: float, bit_depth: int, 
                 start: Timecode, frame_rate: float, drop_frame: bool,
                 number_of_tracks: int, number_of_clips: int, number_of_files: int,
                 online_files: list, offline_files: list, online_clips: list,
                 plug_ins: list, tracks: list, markers: list):
        """Constructor for the Session class
        
        Keyword arguments:
        name: str -- the name of the session
        sample_rate: float -- the sample rate of the session
        bit_depth: int -- the bit depth of the session
        start: Timecode -- the start time of the session
        frame_rate: float -- the frame rate of the session
        drop_frame: bool -- whether the session uses drop frame timecode
        number_of_tracks: int -- the number of tracks in the session
        number_of_clips: int -- the number of clips in the session
        number_of_files: int -- the number of files in the session
        online_files: list -- the online files in the session
        offline_files: list -- the offline files in the session
        online_clips: list -- the online clips in the session
        plug_ins: list -- the plug-ins in the session
        tracks: list -- the tracks in the session
        markers: list -- the markers in the session
        """
        
        self.name = name
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.start = start
        self.frame_rate = frame_rate
        self.drop_frame = drop_frame
        self.number_of_tracks = number_of_tracks
        self.number_of_clips = number_of_clips
        self.number_of_files = number_of_files
        self.online_files = online_files
        self.offline_files = offline_files
        self.online_clips = online_clips
        self.plug_ins = plug_ins
        self.tracks = tracks
        self.markers = markers


    @classmethod
    def from_file(cls, filename: str):
        """Constructor for the Session class using a text file
        
        Keyword arguments:
        filename: str -- the name of the file containing the Pro Tools Marker data
        """
        with open(filename, 'r') as timecode_file:
            content = timecode_file.readlines()

            global_data = Session.extract_global_data(content)

            name = global_data[NAME_INDEX]
            sample_rate = global_data[SAMPLE_RATE_INDEX]
            bit_depth = global_data[BIT_DEPTH_INDEX]
            start = global_data[SESSION_START_INDEX]
            timecode_format = global_data[TIMECODE_FORMAT_INDEX]
            number_of_clips = global_data[NUMBER_OF_CLIPS_INDEX]
            number_of_files = global_data[NUMBER_OF_FILES_INDEX]
            number_of_tracks = global_data[NUMBER_OF_TRACKS_INDEX]

            frame_rate, drop_frame = Session.get_frame_rate(timecode_format)

            sections_data = Session.extract_sections(content)
            
            online_files = sections_data[SectionHeaders.ONLINE_FILES]
            offline_files = sections_data[SectionHeaders.OFFLINE_FILES]
            online_clips = sections_data[SectionHeaders.ONLINE_CLIPS]
            plug_ins = sections_data[SectionHeaders.PLUG_INS_LISTING]
            tracks = sections_data[SectionHeaders.TRACK_LISTING]
            markers = sections_data[SectionHeaders.MARKERS_LISTING]

            return cls(name, sample_rate, bit_depth, start, frame_rate, drop_frame,
                       number_of_tracks, number_of_clips, number_of_files,
                       online_files, offline_files, online_clips, plug_ins,
                       tracks, markers)
                    

    @staticmethod
    def extract_global_data(content: list) -> list:
        """Get the global data from a Pro Tools session file
        
        Keyword arguments:
        content: list -- the content of the Pro Tools session file
        """
        split_global_row = lambda index: re.split(ROW_DELIMITER, content[index])[1]

        name = split_global_row(NAME_INDEX)
        sample_rate = float(split_global_row(SAMPLE_RATE_INDEX))
        bit_depth = int(split_global_row(BIT_DEPTH_INDEX))
        start = Timecode.from_string(split_global_row(SESSION_START_INDEX))
        timecode_format = split_global_row(TIMECODE_FORMAT_INDEX)
        number_of_tracks = int(split_global_row(NUMBER_OF_TRACKS_INDEX))
        number_of_clips = int(split_global_row(NUMBER_OF_CLIPS_INDEX))
        number_of_files = int(split_global_row(NUMBER_OF_FILES_INDEX))

        return [name, sample_rate, bit_depth, start, timecode_format,
                number_of_tracks, number_of_clips, number_of_files]

    @staticmethod
    def get_frame_rate(timecode_format: str) -> float:
        """Get the frame rate from a timecode format
        
        Keyword arguments:
        timecode_format: str -- the timecode format
        """

        frame_rate = float(timecode_format.split(" ")[0])
        drop_frame = bool("Drop" in timecode_format)

        return frame_rate, drop_frame
    
    @staticmethod
    def extract_sections(content: list) -> dict:
        """Get the sections from a Pro Tools session file
        
        Keyword arguments:
        content: list -- the content of the Pro Tools session file
        """
        sections_data = {}
        section_line_index = END_GLOBAL_DATA_INDEX

        def extract_section(header, method):
            nonlocal section_line_index, sections_data, content

            while content[section_line_index] != header.value:
                section_line_index += 1
            
            sections_data[header], section_line_index = method(content, section_line_index)
            
        
        extract_section(SectionHeaders.ONLINE_FILES, Session.extract_online_files)
        extract_section(SectionHeaders.OFFLINE_FILES, Session.extract_offline_files)
        extract_section(SectionHeaders.ONLINE_CLIPS, Session.extract_online_clips)
        extract_section(SectionHeaders.PLUG_INS_LISTING, Session.extract_plug_ins)
        extract_section(SectionHeaders.TRACK_LISTING, Session.extract_tracks)
        extract_section(SectionHeaders.MARKERS_LISTING, Session.extract_markers)

        return sections_data
    
    @staticmethod
    def extract_online_files(content: list, line_index: int) -> tuple:
        return [], line_index
    
    @staticmethod
    def extract_offline_files(content: list, line_index: int) -> tuple:
        return [], line_index
    
    @staticmethod
    def extract_online_clips(content: list, line_index: int) -> tuple:
        return [], line_index
    
    @staticmethod
    def extract_plug_ins(content: list, line_index: int) -> tuple:
        return [], line_index
    
    @staticmethod
    def extract_tracks(content: list, line_index: int) -> tuple:
        return [], line_index
    
    @staticmethod
    def extract_markers(content: list, line_index: int) -> tuple:
        """Get the markers from a Pro Tools session file
        
        Keyword arguments:
        content: list -- the content of the Pro Tools session file
        line_index: int -- the current index of the line being
        """
        line_index += 1
        
        column_headers = Session.extract_section_column_headers(content[line_index], MarkerHeaders)
        line_index += 1

        markers = []

        while content[line_index] != "":
            markers.append(Marker.from_row(content[line_index], column_headers))
            line_index += 1
        
        return markers, line_index
    
    @staticmethod
    def extract_section_column_headers(row: str, headers: Enum) -> dict:
        """Extract the column headers from a section of a Pro Tools session file
        
        Keyword arguments:
        row: str -- the row containing the column headers
        headers: Enum -- the column headers
        """

        row_values = re.split(ROW_DELIMITER, row)
        column_headers = {}

        for i in range(len(row_values)):
            column_headers[headers(i)] = i

        return column_headers