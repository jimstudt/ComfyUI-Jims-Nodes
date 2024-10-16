from .nodes.zoom_focus import *
from .nodes.text_to_string_list import *
from .nodes.dictionaries import *
from .nodes.cubby import *

NODE_CLASS_MAPPINGS = {
    "ZoomFocus" : ZoomFocus,
    "TextToStringList": TextToStringList,
    "ChooseFromStringList": ChooseFromStringList,
    
    "DefineWord": DefineWord,
    "LookupWord": LookupWord,
    "ReplaceWords": ReplaceWords,
    "DictionaryToJSON": DictionaryExport,
    "JSONToDictionary": DefineFromPath,
    "DictFromJSON": DictFromJSON,
    "LoadImageAndInfoFromPath": LoadImageAndInfoFromPath,
    
    "Cubby": Cubby
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZoomFocus": "Zoom On Segment",
    
    "TextToStringList": "Text To String List",
    "ChooseFromStringList": "Choose String",

    "DefineWord": "Define Word",
    "LookupWord": "Lookup Word",
    "ReplaceWords": "Substitute Words",
    "DictionaryToJSON": "Dictionary to JSON",
    "JSONTODictionary": "JSON file to Dictionary",
    "DictFromJSON": "JSON to Dictionary",
    "LoadImageAndInfoFromPath": "Load Image And Info From Path",

    "Cubby" : "CubbyHack"
}
