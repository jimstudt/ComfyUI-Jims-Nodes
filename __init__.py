from .nodes.crop_chest_node import *
from .nodes.text_to_string_list import *
from .nodes.dictionaries import *

NODE_CLASS_MAPPINGS = {
    "CropChest": CropChestNode,

    "TextToStringList": TextToStringList,
    "ChooseFromStringList": ChooseFromStringList,

    "DefineWord": DefineWord,
    "LookupWord": LookupWord,
    "ReplaceWords": ReplaceWords
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CropChest": "Crop to Chest, necklace, not boobs",

    "TextToStringList": "Text To String List",
    "ChooseFromStringList": "Choose String",

    "DefineWord": "Define Word",
    "LookupWord": "Lookup Word",
    "ReplaceWords": "Substitute Words"
}
