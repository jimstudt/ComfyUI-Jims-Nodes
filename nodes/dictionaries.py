
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
    
