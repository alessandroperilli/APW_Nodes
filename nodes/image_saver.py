from ..helpers import any, _get_kw
import torch

#----

import json
import os, sys
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Any
import folder_paths
from PIL import Image, PngImagePlugin

class APW_ImageSaver:

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    # -------------------------- UI --------------------------
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
            "optional": {
                "filename": (
                    "STRING",
                    {"default": "%seed_%date_%time_final_apw", "multiline": False},
                ),
                "path": ("STRING", {"default": "%date/", "multiline": False}),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                    },
                ),
                "image_format": (["png", "jpg", "jpeg", "webp"],),
                "lossless_webp": ("BOOLEAN", {"default": True}),
                "jpg_webp_quality": (
                    "INT",
                    {"default": 100, "min": 1, "max": 100},
                ),
                "date_format": ("STRING", {"default": "%Y-%m-%d", "multiline": False}),
                "time_format": ("STRING", {"default": "%H%M%S", "multiline": False}),
                "generation_notes": ("STRING", {"default": "", "multiline": True}),
                "embed_workflow": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Embeds the complete workflow data into the image metadata. Only works with PNG and WebP formats."
                    }),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("FILENAME", "FILE_PATH")
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "APW Nodes"

    # ---------------------- helpers ------------------------
    @staticmethod
    def _strftime(fmt: str) -> str:
        return datetime.now().strftime(fmt)

    @staticmethod
    def _ensure_list(obj: Any) -> List:
        return obj if isinstance(obj, (list, tuple)) else [obj]

    # ------------------- main routine ----------------------
    def save_images(
        self,
        images,
        filename: str = "%seed_%date_%time_final_meta",
        path: str = "%date/",
        seed: int = 0,
        image_format: str = "png",
        lossless_webp: bool = True,
        jpg_webp_quality: int = 100,
        date_format: str = "%Y-%m-%d",
        time_format: str = "%H%M%S",
        embed_workflow: bool = True,
        generation_notes: str = "",
        extra_pnginfo=None,
    ):
        (
            full_output_folder,
            filename_alt,
            counter_alt,
            subfolder_alt,
            filename_prefix,
        ) = folder_paths.get_save_image_path(
            self.prefix_append,
            self.output_dir,
            images[0].shape[1],
            images[0].shape[0],
        )

        output_folder = Path(full_output_folder)
        counter_base = counter_alt

        base_vars = {
            "%date": self._strftime(date_format),
            "%time": self._strftime(time_format),
            "%seed": seed,
            "%image_format": image_format,
        }

        saved_filenames, saved_paths, ui_images = [], [], []

        for idx, img in enumerate(images):
            var_map = base_vars.copy()
            var_map["%counter"] = f"{counter_base + idx:05}"

            rel_folder = self._replace_tokens(path, var_map)
            rel_filename = self._replace_tokens(filename, var_map)

            final_folder = output_folder / rel_folder
            final_folder.mkdir(parents=True, exist_ok=True)

            full_path = final_folder / f"{rel_filename}.{image_format}"

            pil_img = self._to_pil(img)

            self.process_image(
                pil_img,
                full_path,
                image_format,
                lossless_webp,
                jpg_webp_quality,
                embed_workflow,
                generation_notes,
                seed,
                extra_pnginfo=extra_pnginfo,
            )

            saved_filenames.append(full_path.name)
            saved_paths.append(str(full_path))
            ui_images.append(
                {
                    "filename": full_path.name,
                    "subfolder": str(rel_folder),
                    "type": self.type,
                }
            )

            print(f"[APW_ImageSaver] Saved: {full_path}")

        return {
            "ui": {"images": ui_images},
            "result": (self._single_or_list(saved_filenames), self._single_or_list(saved_paths)),
        }

    # -------------------- internals ------------------------
    @staticmethod
    def _single_or_list(lst):
        return lst[0] if len(lst) == 1 else lst

    @staticmethod
    def _replace_tokens(template: str, mapping: dict) -> str:
        for k, v in mapping.items():
            template = template.replace(k, str(v))
        return template.strip("/")

    @staticmethod
    def _to_pil(img):
        # Already PIL?
        if isinstance(img, Image.Image):
            return img

        try:
            if isinstance(img, torch.Tensor):

                i = 255. * img.cpu().numpy()
                
                # Handle batch dimension - squeeze any singleton dimensions
                while i.ndim > 3:
                    i = i.squeeze(0)
                    
                return Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            elif isinstance(img, np.ndarray):
                # Handle numpy arrays
                arr = (img * 255.0) if img.max() <= 1.0 else img
                
                # Handle batch dimension - squeeze any singleton dimensions
                while arr.ndim > 3:
                    arr = arr.squeeze(0)
                    
                return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
            else:
                raise TypeError(f"Unsupported image data type: {type(img)}")
                
        except Exception as e:
            raise RuntimeError(f"APW_ImageSaver: failed to convert {type(img)} - {str(e)}") from e

    @staticmethod
    def process_image(
        img: Image.Image,
        path: Path,
        image_format: str,
        lossless_webp: bool,
        quality: int,
        embed_workflow: bool,
        generation_notes: str,
        seed: int,
        extra_pnginfo=None,
    ):

        if image_format == "png":
            pnginfo = PngImagePlugin.PngInfo()
            if embed_workflow and extra_pnginfo is not None:
                workflow_json = json.dumps(extra_pnginfo["workflow"])
                pnginfo.add_text("workflow", workflow_json)
            if generation_notes:
                pnginfo.add_text("generation_notes", generation_notes)
            pnginfo.add_text("seed", str(seed))
            img.save(path, pnginfo=pnginfo)
        elif image_format in {"jpg", "jpeg"}:
            img.convert("RGB").save(path, quality=quality)
        elif image_format == "webp":
            img.save(path, "WEBP", lossless=lossless_webp, quality=quality)
        else:
            raise ValueError(f"Unsupported image_format: {image_format}")

#----


NODE_CLASS_MAPPINGS = {
    "APW_ImageSaver": APW_ImageSaver,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APW_ImageSaver": "Image Saver",
}