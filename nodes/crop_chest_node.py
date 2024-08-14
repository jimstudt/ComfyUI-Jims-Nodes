
#
# What I know about SEGS.
#
# I think it is a tuple of a SEG_HEADER and a SEG_ELT, which is why the code
# is always talking about 'segs[1]', that is getting the SEG_ELT. Or maybe an array of them?
#
# 
# 
class CropChestNode:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):

        
        return {
            'required': {
                'image': ("IMAGE", {} ),
                'segs': ("SEGS", {}) ,
                'aspect_ratio': ("INT", {"default": 1, "min": 1, "max": 2}),
            }
        }

    RETURN_TYPES = ( "IMAGE", )

    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Jims/Zoom"

    def execute(self, image, segs, aspect_ratio):
        seg_hdr = segs[0]
        seg_elts = segs[1]
        largest_face = self.find_largest_face(seg_elts)
        if largest_face is None:
            return {"output_image": image}

        bounding_box = largest_face.bbox
        aspect_ratio = 5/7
        crop_box = self.compute_crop_box(bounding_box, aspect_ratio)
        print(f"crop={crop_box}")
        
        cropped_image = self.crop_image(image, crop_box)

        return ( cropped_image,)

    def find_largest_face(self, seg_elts):
        largest_face = None
        max_area = 0
        for face in seg_elts:
            print(f"face={face}")
            area = self.compute_area(face)
            if area > max_area:
                max_area = area
                largest_face = face
        return largest_face

    def compute_area(self, elt):
        # just use bbox for now, search codebase for a better function
        bbox = elt.bbox
        area = ( bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

        print(f"area={area}")

        return area


    def compute_crop_box(self, bounding_box, aspect_ratio):
        x_min, y_min, x_max, y_max = bounding_box
        face_height = y_max - y_min
        extended_y_max = y_max + face_height
        center_x = (x_min + x_max) // 2
        center_y = (y_min + extended_y_max) // 2

        crop_height = extended_y_max - y_min
        crop_width = crop_height * aspect_ratio

        x_crop_min = center_x - crop_width // 2
        x_crop_max = center_x + crop_width // 2
        y_crop_min = y_min
        y_crop_max = y_min + crop_height

        return x_crop_min, y_crop_min, x_crop_max, y_crop_max

    def crop_image(self, image, crop_box):
        x_min, y_min, x_max, y_max = map(int, crop_box)

        wid = image.shape[2]
        hgt = image.shape[1]
        
        x_min = max( x_min, 0)
        x_max = min( x_max, wid - 1)

        y_min = max( y_min, 0)
        y_max = min( y_max, hgt - 1)

        # as god is my witness, I have no idea what this line does, but I copied it from ImageCrop.
        img = image[:,y_min:y_max, x_min:x_max, :]

        return img
