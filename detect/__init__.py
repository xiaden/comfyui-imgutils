"""imgutils_nodes detect sub-package — object detection and OCR (both produce bounding boxes)."""

from .node_detect import ImgUtilsDetect
from .node_ocr import ImgUtilsOCR

NODE_CLASSES = [ImgUtilsDetect, ImgUtilsOCR]
