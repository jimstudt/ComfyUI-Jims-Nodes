
import math

#
# What I know about SEGS.
#
# I think it is a tuple of a SEG_HEADER and a SEG_ELT, which is why the code
# is always talking about 'segs[1]', that is getting the SEG_ELT. Or maybe an array of them?
#
# 
# 
class ZoomFocus:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):

        
        return {
            'required': {
                'image': ("IMAGE", {} ),
                'segs': ("SEGS", {}) ,
                # mode?  Biggest,central,union
                #'aspect_ratio': ("INT", {"default": 1, "min": 1, "max": 2}),
                'megapixels': ("FLOAT", {"default":1.0 }),
                'left_pad_percent': ("INT", { "default": 0}),
                'right_pad_percent': ("INT", { "default": 0}),
                'top_pad_percent': ("INT", { "default": 0}),
                'bottom_pad_percent': ("INT", { "default": 0}),
            },
        }

    RETURN_TYPES = ( "IMAGE", "FLOAT" )
    RETURN_NAMES = ( "image", "upscale-by" )
    
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Jims/Zoom"

    def execute(self, image, segs, megapixels, left_pad_percent, right_pad_percent, top_pad_percent, bottom_pad_percent):
        seg_hdr = segs[0]
        seg_elts = segs[1]
        largest_seg = self.find_largest_seg(seg_elts)
        if largest_seg is None:
            return ( image, 1.0)

        # just do the biggest for now
        bounding_box = largest_seg.bbox

        crop_box = self.compute_crop_box(image, bounding_box, left_pad_percent/100, right_pad_percent/100, top_pad_percent/100, bottom_pad_percent/100)

        # figure upscale
        area = (crop_box[2] - crop_box[0]) * (crop_box[3] - crop_box[1])
        upscale = math.sqrt( (1024*1024*megapixels)/area)
        print(f"Upscale={upscale}")
        
        cropped_image = self.crop_image(image, crop_box)

        return ( cropped_image, upscale)

    def find_largest_seg(self, seg_elts):
        largest_seg = None
        max_area = 0
        for seg in seg_elts:
            area = self.compute_area(seg)
            if area > max_area:
                max_area = area
                largest_seg = seg
        return largest_seg

    def compute_area(self, elt):
        # just use bbox for now, search codebase for a better function
        bbox = elt.bbox
        area = ( bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

        return area


    # that pads are ratios of the width or height, eg. 0=none 0.25=add a quarter of the dimension
    def compute_crop_box(self, image, target__box, left_pad, right_pad, top_pad, bottom_pad):
        image_width = image.shape[2]
        image_height = image.shape[1]
        
        x_min, y_min, x_max, y_max = target__box
        height = y_max - y_min
        width = x_max - x_min

        return ( max(0, x_min - width * left_pad),
                 max(0, y_min - height * top_pad),
                 min(image_width, x_max + width * right_pad),
                 min(image_height, y_max + height * bottom_pad) )

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
