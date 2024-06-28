from Captions.TimeFormats.Nodes.INode import INode
from Captions.TextFormats.ICaption import ICaption

class AbstractCaptionFactory:
    def __init__(self):
        pass

    def create_captions_from_text_and_node(self, text: str, node: INode) -> list[ICaption]:
        pass