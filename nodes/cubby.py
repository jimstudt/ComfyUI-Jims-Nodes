from PIL import Image, ImageOps
import json

class Cubby:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'image_path': ( "STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    INPUT_IS_LIST = False

    FUNCTION = "execute"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False,)
    CATEGORY = "Jims/Text"

    def execute(self, image_path, ):
        img = Image.open(image_path)

        if pr := img.info.get("prompt",None):
            if j := json.loads(pr):
                if positive := j.get("257", {}).get("inputs", {}).get("text2"):
                    return ( positive, )

        return ("",)

