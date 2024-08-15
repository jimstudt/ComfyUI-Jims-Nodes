from .nodes.crop_chest_node import *
from .nodes.zoom_focus import *
from .nodes.text_to_string_list import *
from .nodes.dictionaries import *

NODE_CLASS_MAPPINGS = {
    "CropChest": CropChestNode,

    "ZoomFocus" : ZoomFocus,
    "TextToStringList": TextToStringList,
    "ChooseFromStringList": ChooseFromStringList,

    "DefineWord": DefineWord,
    "LookupWord": LookupWord,
    "ReplaceWords": ReplaceWords
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CropChest": "Crop to Chest, necklace, not boobs",

    "ZoomFocus": "Zoom On Segment",
    
    "TextToStringList": "Text To String List",
    "ChooseFromStringList": "Choose String",

    "DefineWord": "Define Word",
    "LookupWord": "Lookup Word",
    "ReplaceWords": "Substitute Words"
}
