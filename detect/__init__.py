"""imgutils_nodes detect sub-package — object detection and OCR (both produce bounding boxes)."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_detect", "ImgUtilsDetect", "Imgutils Detect"),
    ("node_ocr", "ImgUtilsOCR", "Imgutils OCR"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
