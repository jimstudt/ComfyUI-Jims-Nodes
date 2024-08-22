
#
# These are intended be used thusly...
#
# - At the beginning of your graph, pick a bunch of randomized strings
#   for this run
# - Put each one of them into a common dictionary with a distinct key
# - Later, when assembling some text to CLIP encode, run that text through
#   ReaplceWords and expand anything in the dictionary.
# - The nodes have a dictionary pass through, it helps you keep the 'reroute'
#   clutter down if you wish.
#
# It keeps your prompt text more legible by keeping all the random choosing
# out of it, but it is critical when you want to have different CLIP text for
# different phases of the image refinement operation. For instance, if you
# are detailing a cat's fur, you can have a much more focused prompt string, but
# keep the elements critical to fur.
#
from PIL import Image, ImageOps
import torch
import numpy as np
import os
import json
import yaml
import re

class DictionaryExport:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'dictionary': ( "DICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json",)
    OUTPUT_IS_LIST = (False,)
    
    FUNCTION = "execute"
    OUTPUT_NODE = True
    
    CATEGORY = "Jims/Text"

    def execute(self, dictionary):
        return ( json.dumps(dictionary), )
    

class DefineWord:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'key': ( "STRING", {}),
                'value': ( "STRING", {})
            },
            "optional": {
                'dictionary': ( "DICT", {"forceInput": True})
            }
        }

    RETURN_TYPES = ("DICT",)

    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Jims/Text"

    def execute(self, key, value, dictionary = None):
        if dictionary is None:
            dictionary = {}
        else:
            dictionary = dictionary.copy()  # Make a shallow copy of the original dictionary

        dictionary[key] = value

        return (dictionary, )

class LookupWord:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'dictionary': ( "DICT", {"forceInput": True}),
                'word': ( "STRING", {})
            },
            "optional": {
                'default': ( "STRING", {}),
            },
        }

    RETURN_TYPES = ("DICT","STRING")
    RETURN_NAMES = ("dictionary", "string")
    OUTPUT_IS_LIST = (False, False)
    
    FUNCTION = "execute"
    OUTPUT_NODE = True
    
    CATEGORY = "Jims/Text"

    def execute(self, dictionary, word, default = ''):
        val = dictionary.get( word, default)

        # It might not be a string, by I sure am returning a string
        if val is not None and not isinstance(val, str):
            val = 'ERROR'
            print( f"LookupWord '{word}' is not a string.")
            
        # Note: "ui" does nothing.  It would take Javascript somehow for the node.
        #       I can find no documentation.
        return ( dictionary, val,  {"ui": {"chosen": val}} )
    


class ReplaceWords:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'source': ( "STRING", { "multiline": True}),
                'dictionary': ( "DICT", {"forceInput": True})
            },
        }

    RETURN_TYPES = ("DICT", "STRING",)
    RETURN_NAMES = ("dictionary", "result", )
    OUTPUT_IS_LIST = (False, False,)
    
    FUNCTION = "execute"
    OUTPUT_NODE = True
    
    CATEGORY = "Jims/Text"

    def execute(self, source, dictionary, ):
        # going by longest keys first to prevent EYE from matching EYECOLOR
        for key in sorted(dictionary.keys(), key=len, reverse=True):
            value = dictionary[key]

            if not isinstance(value, str):
                value = "NONSTRING"

            source = source.replace(key, value)

        # Note: "ui" does nothing.  It would take Javascript somehow for the node.
        #       I can find no documentation.
        return ( dictionary, source,  {"ui": {"text": source}} )



class DefineFromPath:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'json_path': ( "STRING", {}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("dictionary",)
    OUTPUT_IS_LIST = (False,)

    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Jims/Text"

    def execute(self, json_path):
        try:
            # Open and read the file
            with open(json_path, 'r') as file:
                data = json.load(file)
        
            # Ensure the loaded data is a dictionary
            if not isinstance(data, dict):
                return {}
        
            # Filter out any key-value pairs where the value is not a string
            filtered_data = {k: v for k, v in data.items() if isinstance(v, str)}

            return ( filtered_data, )
    
        except:
            return {}
    
class LoadImageAndInfoFromPath:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'image_path': ( "STRING", {}),
            },
        }

    RETURN_TYPES = ("IMAGE","DICT","DICT","DICT", "DICT")
    RETURN_NAMES = ("image","prompt", "workflow", "extra", "all_info")
    OUTPUT_IS_LIST = (False,False,False,False,False)

    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Jims/Text"

    def execute(self, image_path):
        #
        # Some sociopathic programmer has been making JSON with apostrophes instead of quotes.
        # So this mess is to catch him and fix it.  It also handles where the JSON has been double encoded
        # as a string.Because that guy really is a sociopath.
        #
        def decode_sloppy_json(source, fix = True):
            try:
                result = json.loads(source)
                if isinstance(result, str):
                    return decode_sloppy_json(result)  # If result is a string, try to decode it again
                return result
            except json.JSONDecodeError:
                if not fix:
                    raise 
                corrected_source = re.sub(r"(?<!\\)'", '"', source)
                return decode_sloppy_json( corrected_source, fix = False)


        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File '{image_path}' cannot be found.")

        if image := Image.open(image_path):
            image = ImageOps.exif_transpose(image)
            img = image.convert("RGB")
            img = np.array(img).astype(np.float32) / 255.0
            img = torch.from_numpy(img)[None,]


            if info := image.info:
                prompt = decode_sloppy_json( info.get("prompt","{}"))
                workflow = decode_sloppy_json( info.get("workflow","{}"))
                extra = decode_sloppy_json( info.get("extra","{}"))

                return { "result": ( img, prompt, workflow, extra, info.copy()) }

            else:
                return { "result":(img, {},{},{}, {}) }

        raise ValueError(f"Can't open image: {image_path}")
