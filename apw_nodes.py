import torch

class AnyType(str):
    def __ne__(self, __value: object) -> bool:  
        return False

any = AnyType("*")

#---------------------------------------------------------------------------------------------------------------------#

class APW_LocalImageSize:

    @classmethod
    def INPUT_TYPES(cls):
        image_presets = [
            "custom",
            "--------- FLUX.1, SD 3.5 ---------",
            "1152x1728 (2:3 | 2MP)",
            "1216x1664 (3:4 | 2MP)",
            "1728x1152 (3:2 | 2MP)",
            "1664x1216 (4:3 | 2MP)",
            "1920x1088 (16:9 | 2MP)",
            "2176x960 (21:9 | 2MP)",
            "1408x1408 (1:1 | 2MP)",
            "----- FLUX.1, SD 3.5, SDXL -----",
            "896x1152 (3:4 | 1MP)",
            "832x1216 (5:8 | 1MP)",
            "1152x896 (4:3 | 1MP)",
            "1216x832 (3:2 | 1MP)",
            "1344x768 (16:9 | 1MP)",
            "1536x640 (21:9 | 1MP)",
            "1024x1024 (1:1 | 1MP)",
            "------------- SD 1.5 ---------------",
            "512x768 (2:3 | 0.4MP)",
            "512x682 (3:4 | 0.3MP)",
            "768x512 (3:2 | 0.4MP)",
            "682x512 (4:3 | 0.3MP)",
            "910x512 (16:9 | 0.5MP)",
            "952x512 (1.85:1 | 0.5MP)",
            "512x512 (1:1 | 0.3MP)",
        ]

        return {
            "required": {
                "image_width":  ("INT", {"default": 64, "min": 64, "max": 8192}),
                "image_height": ("INT", {"default": 64, "min": 64, "max": 8192}),
                "image_aspect_ratio": (image_presets,),

                "batch_size":  ("INT", {"default": 1, "min": 1,  "max": 64}),
            }
        }

    # ──────────────────────────────────────────────────────────────────────────
    # OUTPUT SPECIFICATION
    # ──────────────────────────────────────────────────────────────────────────
    RETURN_TYPES = (
        "INT",    # image_width
        "INT",    # image_height
        "LATENT", # image_latent
        "INT",    # batch_size
    )

    RETURN_NAMES = (
        "image_width",
        "image_height",
        "image_latent",
        "batch_size",
    )

    FUNCTION = "configure_sizes"
    CATEGORY = "APW Nodes"

    _IMAGE_MAP = {
        "1152x1728 (2:3 | 2MP)": (1152, 1728),
        "1216x1664 (3:4 | 2MP)": (1216, 1664),
        "1728x1152 (3:2 | 2MP)": (1728, 1152),
        "1664x1216 (4:3 | 2MP)": (1664, 1216),
        "1920x1088 (16:9 | 2MP)": (1920, 1088),
        "2176x960 (21:9 | 2MP)": (2176, 960),
        "1408x1408 (1:1 | 2MP)": (1408, 1408),
        "896x1152 (3:4 | 1MP)": (896, 1152),
        "832x1216 (5:8 | 1MP)": (832, 1216),
        "1152x896 (4:3 | 1MP)": (1152, 896),
        "1216x832 (3:2 | 1MP)": (1216, 832),
        "1344x768 (16:9 | 1MP)": (1344, 768),
        "1536x640 (21:9 | 1MP)": (1536, 640),
        "1024x1024 (1:1 | 1MP)": (1024, 1024),
        "512x768 (2:3 | 0.4MP)": (512, 768),
        "512x682 (3:4 | 0.3MP)": (512, 682),
        "768x512 (3:2 | 0.4MP)": (768, 512),
        "682x512 (4:3 | 0.3MP)": (682, 512),
        "910x512 (16:9 | 0.5MP)": (910, 512),
        "952x512 (1.85:1 | 0.5MP)": (952, 512),
        "512x512 (1:1 | 0.3MP)": (512, 512),
    }

    # ──────────────────────────────────────────────────────────────────────────
    # MAIN LOGIC
    # ──────────────────────────────────────────────────────────────────────────
    def configure_sizes(
        self,
        image_width: int,
        image_height: int,
        image_aspect_ratio: str,
        batch_size: int,
    ):

        # Override custom image dims if preset chosen
        if image_aspect_ratio in self._IMAGE_MAP:
            image_width, image_height = self._IMAGE_MAP[image_aspect_ratio]

        # Latent tensors (SD‑type models require /8 dims)
        image_latent = torch.zeros([batch_size, 4, image_height // 8, image_width // 8])

        return (
            image_width,
            image_height,
            {"samples": image_latent},
            batch_size,
        )

#---------------------------------------------------------------------------------------------------------------------#

class APW_LocalVideoSize:

    @classmethod
    def INPUT_TYPES(cls):
        video_presets = [
            "custom",
            "1360x768 [CogVideoX 1.5]",
            "1280x720 [WanVideo 2.1, Hunyuan Video]",
            "960x544 [Hunyuan Video]",
            "854x480 [WanVideo 2.1]",
            "720x480 [CogVideoX 1.5]",
        ]

        return {
            "required": {
                "video_width":  ("INT", {"default": 64, "min": 64, "max": 8192}),
                "video_height": ("INT", {"default": 64,  "min": 64, "max": 8192}),
                "video_aspect_ratio": (video_presets,),

                "batch_size":  ("INT", {"default": 1, "min": 1,  "max": 64}),
            }
        }

    # ──────────────────────────────────────────────────────────────────────────
    # OUTPUT SPECIFICATION
    # ──────────────────────────────────────────────────────────────────────────
    RETURN_TYPES = (
        "INT",    # video_width
        "INT",    # video_height
        "LATENT", # video_latent
        "INT",    # batch_size
    )

    RETURN_NAMES = (
        "video_width",
        "video_height",
        "video_latent",
        "batch_size",
    )

    FUNCTION = "configure_sizes"
    CATEGORY = "APW Nodes"

    _VIDEO_MAP = {
        "1360x768 [CogVideoX 1.5]": (1360, 768),
        "1280x720 [WanVideo 2.1, Hunyuan Video]":  (1280, 720),
        "960x544 [Hunyuan Video]":  (960, 544),
        "854x480 [WanVideo 2.1]":   (854, 480),
        "720x480 [CogVideoX 1.5]":  (720, 480),
    }

    # ──────────────────────────────────────────────────────────────────────────
    # MAIN LOGIC
    # ──────────────────────────────────────────────────────────────────────────
    def configure_sizes(
        self,
        video_width: int,
        video_height: int,
        video_aspect_ratio: str,
        batch_size: int,
    ):

        # Override custom video dims if preset chosen
        if video_aspect_ratio in self._VIDEO_MAP:
            video_width, video_height = self._VIDEO_MAP[video_aspect_ratio]

        # Latent tensors (SD‑type models require /8 dims)
        video_latent = torch.zeros([batch_size, 4, video_height // 8, video_width // 8])

        return (
            video_width,
            video_height,
            {"samples": video_latent},
            batch_size,
        )

#---------------------------------------------------------------------------------------------------------------------#

class APW_CloudImageSize:

    @classmethod
    def INPUT_TYPES(cls):
        image_presets = [
            # OpenAI GPT-image-1
            "1536x1024 (3:2 | 1.6MP) [GI1]",
            "1024x1536 (2:3 | 1.6MP) [GI1]",
            "1024x1024 (1:1 | 1MP) [GI1]",
        ]

        return {
            "required": {
                "image_width":  ("INT", {"default": 64, "min": 64, "max": 8192}),
                "image_height": ("INT", {"default": 64, "min": 64, "max": 8192}),
                "image_aspect_ratio": (image_presets,),

                "batch_size":  ("INT", {"default": 1, "min": 1,  "max": 64}),
            }
        }

    # ──────────────────────────────────────────────────────────────────────────
    # OUTPUT SPECIFICATION
    # ──────────────────────────────────────────────────────────────────────────
    RETURN_TYPES = (
        "INT",    # image_width
        "INT",    # image_height
        any, # aspect_ratio (dimension string for combo inputs)
        "LATENT", # image_latent
        "INT",    # batch_size
    )

    RETURN_NAMES = (
        "image_width",
        "image_height",
        "aspect_ratio",
        "image_latent",
        "batch_size",
    )

    FUNCTION = "configure_sizes"
    CATEGORY = "APW Nodes"

    # ──────────────────────────────────────────────────────────────────────────
    # INTERNAL MAPPINGS
    # ──────────────────────────────────────────────────────────────────────────
    _IMAGE_MAP = {
        "1536x1024 (3:2 | 1.6MP) [GI1]": (1536, 1024),
        "1024x1536 (2:3 | 1.6MP) [GI1]": (1024, 1536),
        "1024x1024 (1:1 | 1MP) [GI1]": (1024, 1024),
    }

    # ──────────────────────────────────────────────────────────────────────────
    # MAIN LOGIC
    # ──────────────────────────────────────────────────────────────────────────
    def configure_sizes(
        self,
        image_width: int,
        image_height: int,
        image_aspect_ratio: str,
        batch_size: int,
    ):

        # Override custom image dims if preset chosen
        if image_aspect_ratio in self._IMAGE_MAP:
            image_width, image_height = self._IMAGE_MAP[image_aspect_ratio]

        # Latent tensors (SD‑type models require /8 dims)
        image_latent = torch.zeros([batch_size, 4, image_height // 8, image_width // 8])

        # Pure dimension string for combo output (first token before space)
        aspect_str = f"{image_width}x{image_height}" if image_aspect_ratio == "custom" else image_aspect_ratio.split(" ")[0]

        return (
            image_width,
            image_height,
            aspect_str,
            {"samples": image_latent},
            batch_size,
        )
    
#---------------------------------------------------------------------------------------------------------------------#

class APW_ImageListFilter:
    """
    Passes through or removes images from an IMAGE list according
    to a minimum width / height. “0” means “no limit” for that dimension.

    • width_min: images with width  ≤ width_min  are dropped
    • height_min: images with height ≤ height_min are dropped

    If *all* images are dropped and a ``fallback_image`` is supplied, the node
    outputs a single‑element IMAGE list containing that fallback image.
    The fallback tensor is normalised (uint8 → float32 0‑1) and guaranteed to
    have an explicit batch‑dimension so that downstream nodes and PIL previews
    can handle it without raising a *Cannot handle this data type* error.
    """

    INPUT_IS_LIST = True
    RETURN_TYPES = ("IMAGE", "STRING")
    OUTPUT_IS_LIST = (True, False)
    RETURN_NAMES = ("images", "removed_indices")
    FUNCTION = "filter"
    CATEGORY = "APW Nodes"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "width_min": ("INT", {"default": 0, "min": 0}),
                "height_min": ("INT", {"default": 0, "min": 0}),
            },
            "optional": {
                "fallback_image": ("IMAGE",),
            },
        }

    def _ensure_tensor_4d_float(self, img):
        """Make sure *img* is float32 with shape (1, H, W, C)."""
        if isinstance(img, list):  # Unwrap widget lists
            img = img[0]
        if img.ndim == 3:          # (H, W, C) → add batch dim
            img = img.unsqueeze(0)
        if img.dtype == torch.uint8:  # uint8 0‑255 → float32 0‑1
            img = img.to(torch.float32).div(255.0)
        return img

    def filter(self,
               images,
               width_min,
               height_min,
               fallback_image=None):

        # unwrap scalar widget lists (Comfy wraps INT widgets in 1‑elem lists)
        if isinstance(width_min, list):
            width_min = width_min[0]
        if isinstance(height_min, list):
            height_min = height_min[0]

        # Convert optional fallback right away so it’s ready if needed
        if fallback_image is not None:
            fallback_image = self._ensure_tensor_4d_float(fallback_image)

        # user entry N means “keep ≥ N+1” (to match original semantics)
        width_thr = width_min + 1 if width_min else 0
        height_thr = height_min + 1 if height_min else 0

        kept, removed = [], []

        for idx, img in enumerate(images):
            _, H, W, _ = img.shape  # B, H, W, C

            if (width_thr and W < width_thr) or (height_thr and H < height_thr):
                removed.append(idx)
            else:
                kept.append(img)

        # If nothing survived, fall back to a single image when provided
        if not kept and fallback_image is not None:
            kept.append(fallback_image)

        return kept, ", ".join(map(str, removed))