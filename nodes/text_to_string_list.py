
import random

#
# 
# 
class TextToStringList:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):

        
        return {
            'required': {
                'text': ( "STRING", {"default": '# comments begin like this\n# white space is trimmed\n# blank lines are dropped\n', "multiline": True}),
            },
            'optional': {
                'prefix': ( "STRING", { "forceInput": True } ),
            }
        }

    RETURN_TYPES = ("STRING",)
    INPUT_IS_LIST = True

    FUNCTION = "execute"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Jims/Text"

    def execute(self, text, prefix = [] ):
        # I hate this, but I can't get it to have text be a string and prefix be a list of strings, so they are
        # both lists now.
        text = '\n'.join(text)

        print( text, prefix)
        result = [
            stripped_line
            for line in text.splitlines()
            if (stripped_line := line.strip()) and not stripped_line.startswith('#')
        ]

        # probably should strip the non-strings from prefix
        
        return ( prefix + result,)

class ChooseFromStringList:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):

        
        return {
            'required': {
                'strings': ( "STRING", {"forceInput": True} ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    INPUT_IS_LIST = (True, False)
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("strings", "chosen")
    OUTPUT_IS_LIST = (True, False)

    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Jims/Text"

    def execute(self, strings, seed):
        if list:
            choice = random.choice( strings)
        else:
            choice = ""

        return {"ui": {"text": (choice,)}, "result": (strings,choice,)}


