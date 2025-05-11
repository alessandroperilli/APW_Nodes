from .apw_nodes import APW_ImageListFilter, APW_LocalImageSize, APW_CloudImageSize, APW_LocalVideoSize

NODE_CLASS_MAPPINGS = {
    "APW_ImageListFilter": APW_ImageListFilter,
    "APW_LocalImageSize": APW_LocalImageSize,
    "APW_CloudImageSize": APW_CloudImageSize,
    "APW_LocalVideoSize": APW_LocalVideoSize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APW_ImageListFilter": "Image List Filter",
    "APW_LocalImageSize": "Image Size (Local Models)",
    "APW_CloudImageSize": "Image Size (Cloud Models)",
    "APW_LocalVideoSize": "Video Size (Local Models)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]