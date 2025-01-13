import torch

class ImageToSolidBackground:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "Custom/Image Processing"

    @staticmethod
    def process(image, mask):
        """
        Process a batch of images and masks.
        """


        output_images = torch.stack([
            ImageToSolidBackground.doImage(img, msk)
            for img, msk in zip(image, mask)
        ])  # Shape: [batch, height, width, 3]

        return (output_images,)

    @staticmethod
    def doImage( image_t, mask_t):
        mask = ~mask_t.bool()

        print(f"mask={mask.shape}")
        print(f"image={image_t.shape}")

        if not mask.any():
            print("mask is empty")
            # Default to white if no region is selected
            average_color = torch.tensor([255, 255, 255], dtype=torch.uint8)
        else:
            # Get selected pixels from the image
            selected_colors = image_t[mask]  # Shape: [N, 3]
            unique_colors,counts = torch.unique( selected_colors, dim=0, return_counts=True)
            average_color = unique_colors[ torch.argmax(counts) ]
            
            print(f"color={average_color}")
            

        return average_color.expand_as(image_t)


class LiftFromBackground:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "background": ("IMAGE",),
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "process"
    CATEGORY = "Custom/Image Processing"

    @staticmethod
    def process(image, background, mask):
        """
        Takes an image, background, and mask and computes the RGBA output.
        """
        # Don't do batches, just take the singleton element
        image_tensor = image[0]
        background_tensor = background[0]
        mask_tensor = mask[0]

        print(f"Image shape: {image_tensor.shape} of {image_tensor.dtype}")
        print(f"Background shape: {background_tensor.shape} of {background_tensor.dtype}")
        print(f"Mask shape: {mask_tensor.shape} of {mask_tensor.dtype}")
        
        # Check for matching dimensions
        if image_tensor.shape != background_tensor.shape or image_tensor.shape[:2] != mask_tensor.shape:
            raise ValueError("Image, background, and mask must have the same width and height.")

        height, width, _ = image_tensor.shape

        # Create the output tensors
        result_image = torch.zeros_like(image_tensor)
        result_alpha = torch.zeros((height, width), dtype=torch.float32)

        dull_red = torch.tensor( [0.25, 0, 0], dtype=torch.float32 ).to( image_tensor.dtype)
        
        # Process each pixel
        for y in range(height):
            for x in range(width):
                if mask_tensor[y, x]:  # In mask: use image pixel and alpha 1.0
                    result_image[y, x] = image_tensor[y, x]
                    result_alpha[y, x] = 1.0
                else:  # Not in mask: compute minimum alpha to match the image pixel
                    need_alpha = torch.zeros_like( image_tensor[y,x])
                    
                    for ch in range(3):
                        i = image_tensor[y,x,ch]
                        bg = background_tensor[y,x,ch]

                        if i == bg:
                            continue    # zero is fine

                        if i > bg:
                            need_alpha[ch] = (i - bg)/( 1.0 - bg) # i > bg :: bg != 1
                        else:
                            need_alpha[ch] = 1 - i / bg           # i < bg :: bg != 0

                    # We use the highest required alpha so all channels can get a solution
                    alpha = need_alpha.max()

                    for ch in range(3):
                        i = image_tensor[y,x,ch]
                        bg = background_tensor[y,x,ch]

                        result_image[y,x,ch] = i/alpha - bg/alpha + bg

                    result_alpha[y,x] = alpha

        # Add back the batch dimension (singleton batch)
        result_image = result_image.unsqueeze(0)  # Shape: [1, height, width, 3]
        result_alpha = result_alpha.unsqueeze(0)  # Shape: [1, height, width]

        return result_image, result_alpha
