import re
from enum import Enum

from ProTools.Marker import Marker, ColumnHeaders as MarkerHeaders
from ProTools.EDL import EDL, ColumnHeaders as EDLHeaders
from ProTools.File import File, ColumnHeaders as FileHeaders
from ProTools.Clip import Clip, ColumnHeaders as ClipHeaders
from ProTools.Plugin import Plugin, ColumnHeaders as PluginHeaders
from ProTools.Track import Track
from ProTools.Timecode import Timecode
import ProTools.lib as lib

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

    @classmethod
    def header_exists(cls, header: str):
        return header in cls._value2member_map_ 

class Session:
    def __init__(self, name: str, sample_rate: float, bit_depth: BitDepths, 
                 start: Timecode, frame_rate: float, drop_frame: bool,
                 number_of_tracks: int, number_of_clips: int, number_of_files: int,
                 online_files: list, offline_files: list, online_clips: list,
                 plug_ins: list, tracks: list[Track], markers: list):
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

            # Parse the global data
            globals = cls.parse_globals(content[NAME_INDEX:END_GLOBAL_DATA_INDEX])

            name = globals[NAME_INDEX]
            sample_rate = globals[SAMPLE_RATE_INDEX]
            bit_depth = BitDepths(globals[BIT_DEPTH_INDEX].strip())
            start = globals[SESSION_START_INDEX]
            timecode_format = globals[TIMECODE_FORMAT_INDEX]
            number_of_clips = globals[NUMBER_OF_CLIPS_INDEX]
            number_of_files = globals[NUMBER_OF_FILES_INDEX]
            number_of_tracks = globals[NUMBER_OF_TRACKS_INDEX]

            frame_rate, drop_frame = cls.get_frame_rate(timecode_format)

            # Parse the rest of the file
            sections = cls.split_sections(content[END_GLOBAL_DATA_INDEX:])

            parse = lambda header, parser: parser(sections[header]) if header in sections else []

            online_files = parse(SectionHeaders.ONLINE_FILES, cls.parse_files)
            offline_files = parse(SectionHeaders.OFFLINE_FILES, cls.parse_files)
            online_clips = parse(SectionHeaders.ONLINE_CLIPS, cls.parse_clips)
            plug_ins = parse(SectionHeaders.PLUG_INS_LISTING, cls.parse_plugins)
            tracks = parse(SectionHeaders.TRACK_LISTING, cls.parse_tracks)
            markers = parse(SectionHeaders.MARKERS_LISTING, cls.parse_markers)
            
            return cls(name, sample_rate, bit_depth, start, frame_rate, drop_frame,
                       number_of_tracks, number_of_clips, number_of_files,
                       online_files, offline_files, online_clips, plug_ins,
                       tracks, markers)
                

    @staticmethod
    def parse_globals(content: list) -> list:
        """Get the global data from a Pro Tools session file
        
        Keyword arguments:
        content: list -- the content of the Pro Tools session file
        """
        split_global_row = lambda index: re.split(ROW_DELIMITER, content[index])[1]

        name = split_global_row(NAME_INDEX)
        sample_rate = float(split_global_row(SAMPLE_RATE_INDEX))
        bit_depth = split_global_row(BIT_DEPTH_INDEX)
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
    def split_sections(content: list) -> dict[SectionHeaders, list]:
        """Extract the sections from a Pro Tools session file
        
        Keyword arguments:
        content: list -- the content of the Pro Tools session file
        """
        sections = {}

        for line_index in range(len(content)):
            line = content[line_index].strip()
            if SectionHeaders.header_exists(line):
                section_header = SectionHeaders(line)
                section_content = []

                line_index += 1

                while (line_index < len(content) 
                       and not SectionHeaders.header_exists(content[line_index])):
                    line = content[line_index].strip()

                    if line != "":
                        section_content.append(content[line_index])

                    line_index += 1

                sections[section_header] = section_content

        return sections


    @classmethod
    def parse_section(cls, content: list, HeaderType: Enum, constructor: callable) -> list:
        """Parse a section of a Pro Tools session file
        
        Keyword arguments:
        sections: dict -- the sections of the Pro Tools session file
        header: SectionHeaders -- the header of the section to parse
        parse: callable -- the function to parse the section
        """
        TITLE_INDEX = 0
        COLUMN_HEADER_INDEX = 1
        DATA_INDEX = 2
        
        column_headers = lib.parse_column_headers(content[COLUMN_HEADER_INDEX], HeaderType)
        section = []

        for row in content[DATA_INDEX:]:
            if row != "":
                section.append(constructor(column_headers, row))

        return section


    @classmethod
    def parse_files(cls, content: list) -> list:
        """Wrapper function to parse the files in a Pro Tools session file"""
        return cls.parse_section(content, FileHeaders, File.from_row)
    

    @classmethod
    def parse_clips(cls, content: list) -> list:
        """Wrapper function to parse the clips in a Pro Tools session file"""
        # TODO: Implement
        return []
    

    @classmethod
    def parse_plugins(cls, content: list) -> list:
        """Wrapper function to parse the plugins in a Pro Tools session file"""
        # TODO: Implement
        return []
    

    @classmethod
    def parse_tracks(cls, content: list) -> list:
        """Parse the tracks in a Pro Tools session file"""

        NAME_INDEX = 0
        COLUMN_HEADERS_INDEX = 4
        
        track_start_index = NAME_INDEX
        tracks = []

        column_headers = lib.parse_column_headers(content[COLUMN_HEADERS_INDEX], EDLHeaders)

        for line_index in range(NAME_INDEX+1, len(content)):
            line = lib.split_row(content[line_index])[0]
            if line == "TRACK NAME:":
                tracks.append(Track.from_rows(column_headers, content[track_start_index:line_index]))
                track_start_index = line_index
        
        tracks.append(Track.from_rows(column_headers, content[track_start_index:]))

        return tracks
    
    
    @classmethod
    def parse_markers(cls, content: list) -> list:
        """Wrapper function to parse the markers in a Pro Tools session file"""
        return cls.parse_section(content, MarkerHeaders, Marker.from_row)
    