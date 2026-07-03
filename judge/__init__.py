"""imgutils_nodes validate sub-package."""
from __future__ import annotations

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .node_classify import ImgUtilsClassify
    NODE_CLASS_MAPPINGS["ImgUtilsClassify"] = ImgUtilsClassify
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsClassify"] = "Imgutils Classify"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsClassify unavailable", exc_info=True)

try:
    from .node_check import ImgUtilsCheck
    NODE_CLASS_MAPPINGS["ImgUtilsCheck"] = ImgUtilsCheck
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCheck"] = "Imgutils Check"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsCheck unavailable", exc_info=True)

try:
    from .node_metric import ImgUtilsMetric
    NODE_CLASS_MAPPINGS["ImgUtilsMetric"] = ImgUtilsMetric
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsMetric"] = "Imgutils Metric"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsMetric unavailable", exc_info=True)
