"""imgutils_nodes transform sub-package — CDC upscaling, censoring, alignment, and squeeze-crop."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_cdc", "ImgUtilsCDC", "Imgutils Upscale (CDC)"),
    ("node_censor", "ImgUtilsCensor", "Imgutils Censor"),
    ("node_align", "ImgUtilsAlign", "Imgutils Align"),
    ("node_squeeze", "ImgUtilsSqueeze", "Imgutils Squeeze"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
