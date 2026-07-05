"""imgutils_nodes judge sub-package — classification, boolean checks, and quality metrics."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_classify", "ImgUtilsClassify", "Imgutils Classify"),
    ("node_check", "ImgUtilsCheck", "Imgutils Check"),
    ("node_metric", "ImgUtilsMetric", "Imgutils Metric"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
