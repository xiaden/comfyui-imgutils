"""imgutils_nodes segment sub-package — character segmentation and background removal."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_segment", "ImgUtilsSegment", "Imgutils Segment"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
