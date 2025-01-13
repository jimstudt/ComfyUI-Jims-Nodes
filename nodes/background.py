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
        Takes an image, background, and mask and computes the RGBA output using broadcasting.
        """
        # Remove the batch dimension (singleton batch)
        image_tensor = image[0]  # Shape: [h, w, 3]
        background_tensor = background[0]  # Shape: [h, w, 3]
        mask_tensor = mask[0]  # Shape: [h, w]

        # Print diagnostic information
        print(f"Image shape: {image_tensor.shape} of {image_tensor.dtype}")
        print(f"Background shape: {background_tensor.shape} of {background_tensor.dtype}")
        print(f"Mask shape: {mask_tensor.shape} of {mask_tensor.dtype}")

        #
        # I am sorry!!!! This was nice legible code that traversed the pixels by rows and columns,
        # but was painfully slow.  I asked ChatGPT to rewrite it to use "broadcasting" in the torch
        # sense.  And now it is this, which is blindingly fast to run, but a bit of a head scratcher to read.
        
        # Check for matching dimensions
        if image_tensor.shape != background_tensor.shape or image_tensor.shape[:2] != mask_tensor.shape:
            raise ValueError("Image, background, and mask must have the same width and height.")

        # Expand the mask to broadcast across RGB channels
        mask_expanded = mask_tensor.unsqueeze(-1).to(torch.float32)  # Shape: [h, w, 1]

        # Compute the needed alpha values
        diff = image_tensor - background_tensor  # Element-wise difference [h, w, 3]
        need_alpha = torch.zeros_like(diff)

        # Case 1: where image == background (alpha = 0)
        #  a null op, there is already a zero in need_alpha for this element.

        # Case 2: where image > background (set result to 1.0)
        brighter_mask = (image_tensor > background_tensor)
        need_alpha[brighter_mask] = (diff[brighter_mask]) / (1.0 - background_tensor[brighter_mask])

        # Case 3: where image < background (set result to 0.0)
        darker_mask = (image_tensor < background_tensor)
        need_alpha[darker_mask] = 1.0 - image_tensor[darker_mask] / background_tensor[darker_mask]

        # At this point, need_alpha [h, w, 3] has the minimum required alpha for each channel of each pixel
        
        # Set alpha to the max across RGB channels
        alpha = torch.clamp(need_alpha.max(dim=-1).values, 0.0, 1.0)  # Shape: [h, w]

        # Compute result image using broadcasting
        alpha_expanded = alpha.unsqueeze(-1)  # Shape: [h, w, 1] for RGB broadcasting
        # NOTE: That 1e-8 makes divide by zero be a huge number instead of an error. The upcoming clamp handles that.
        result_image = (image_tensor - (1.0 - alpha_expanded) * background_tensor) / alpha_expanded.clamp(min=1e-8)
        result_image = torch.clamp(result_image, 0.0, 1.0)  # Clamp to valid range

        # Set final image and alpha in mask regions
        result_image = torch.where(mask_expanded.bool(), image_tensor, result_image)
        alpha = torch.where(mask_tensor.bool(), torch.ones_like(alpha), alpha)

        # Add back the batch dimension
        result_image = result_image.unsqueeze(0)  # Shape: [1, h, w, 3]
        result_alpha = alpha.unsqueeze(0)  # Add back batch dimension

        return result_image, result_alpha
