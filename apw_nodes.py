import torch
from comfy.utils import common_upscale   # ← only needed if you keep the optional replacement logic


class ImageListFilter:
    """
    Passes through or removes images from an IMAGE list according to a
    minimum width / height.  “0” means “no limit” for that dimension.

    • width_min  – images whose width  ≤ width_min  are dropped
    • height_min – images whose height ≤ height_min are dropped

      (The +1 logic below makes the behaviour match your example:
       entering 64 removes images < 65 px.)

    Optional: a replacement_image can be supplied; if present an image
    that would be dropped is instead replaced with that image.
    """

    INPUT_IS_LIST  = True
    RETURN_TYPES   = ("IMAGE", "STRING")
    OUTPUT_IS_LIST = (True, False)
    RETURN_NAMES   = ("images", "removed_indices")
    FUNCTION       = "filter"
    CATEGORY       = "APW Nodes"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),          # list input from MakeImageList
                "width_min":  ("INT", {"default": 0, "min": 0}),
                "height_min": ("INT", {"default": 0, "min": 0}),
            },
            "optional": {
                "replacement_image": ("IMAGE",),
            },
        }

    # ------------------------------------------------------------------
    def filter(self,
               images,
               width_min,
               height_min,
               replacement_image=None):

        # unwrap widget lists (ComfyUI wraps scalar widgets in 1-element lists)
        if isinstance(width_min,  list):  width_min  = width_min[0]
        if isinstance(height_min, list):  height_min = height_min[0]
        if isinstance(replacement_image, list) and replacement_image:
            replacement_image = replacement_image[0]

        # add 1 so “64” really means 65-px threshold as per your example
        width_thr  = width_min  + 1 if width_min  else 0
        height_thr = height_min + 1 if height_min else 0

        kept, removed = [], []

        for idx, img in enumerate(images):
            _, H, W, _ = img.shape   # B=1, H, W, C

            too_narrow = (width_thr  and W < width_thr)
            too_short  = (height_thr and H < height_thr)

            if too_narrow or too_short:
                removed.append(idx)
                if replacement_image is not None:
                    rep = replacement_image
                    # resize rep to match current image if needed
                    if rep.shape[1:3] != img.shape[1:3]:
                        rep = common_upscale(rep.movedim(-1, 1), W, H,
                                             "lanczos", "center").movedim(1, -1)
                    kept.append(rep[0] if rep.ndim == 4 else rep)
                # otherwise drop image
            else:
                kept.append(img)

        return kept, ', '.join(map(str, removed))