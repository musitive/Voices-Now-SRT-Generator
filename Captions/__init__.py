from Captions.AbstractCaptionFactory import AbstractCaptionFactory
from Captions.SRTFactory import SRTFactory
from Captions.SplitterFactory import SplitterFactory

INVALID_DATA_TYPE = "Error: Invalid data type: {0}"

def initialize_caption_factory(file_type: str = "SRT", split: bool = False) -> AbstractCaptionFactory:
    caption_factory = None

    if split == True:
        caption_factory = initialize_splitter_caption_factory(file_type)
    else:
        caption_factory = initialize_unsplit_caption_factory(file_type)
        
    return caption_factory


def initialize_splitter_caption_factory(file_type: str) -> AbstractCaptionFactory:
    unsplit_caption_factory = initialize_unsplit_caption_factory(file_type)
    return SplitterFactory(unsplit_caption_factory)


def initialize_unsplit_caption_factory(file_type: str) -> AbstractCaptionFactory:
    caption_factory = None

    if file_type == "SRT":
        caption_factory = SRTFactory()
    else:
        raise ValueError(INVALID_DATA_TYPE.format(file_type))
    
    return caption_factory