"""
imgutils_nodes — ComfyUI custom node pack wrapping deepghs/imgutils.

Provides 14 nodes for anime image analysis, tagging, detection, and processing.
Uses the ComfyUI V2 io.ComfyNode API.
"""

from __future__ import annotations

import logging

from comfy_api.latest import ComfyExtension, io

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Node imports — wrapped in try/except for graceful degradation
# when optional dependencies (dghs-imgutils) are missing.

try:
    from .node_validate import ImgUtilsValidate

    NODE_CLASS_MAPPINGS["ImgUtilsValidate"] = ImgUtilsValidate
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsValidate"] = "Imgutils Judge"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsValidate unavailable.", exc_info=True)

try:
    from .node_ocr import ImgUtilsOCR

    NODE_CLASS_MAPPINGS["ImgUtilsOCR"] = ImgUtilsOCR
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsOCR"] = "Imgutils OCR"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsOCR unavailable.", exc_info=True)

try:
    from .node_detect import ImgUtilsDetect

    NODE_CLASS_MAPPINGS["ImgUtilsDetect"] = ImgUtilsDetect
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsDetect"] = "Imgutils Detect"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsDetect unavailable.", exc_info=True)

try:
    from .node_transform import ImgUtilsTransform

    NODE_CLASS_MAPPINGS["ImgUtilsTransform"] = ImgUtilsTransform
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsTransform"] = "Imgutils Transform"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsTransform unavailable.", exc_info=True)

try:
    from .node_compare import ImgUtilsCompare

    NODE_CLASS_MAPPINGS["ImgUtilsCompare"] = ImgUtilsCompare
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCompare"] = "Imgutils Compare"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsCompare unavailable.", exc_info=True)

try:
    from .node_pose import ImgUtilsPose

    NODE_CLASS_MAPPINGS["ImgUtilsPose"] = ImgUtilsPose
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsPose"] = "Imgutils Pose"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsPose unavailable.", exc_info=True)

try:
    from .node_segment import ImgUtilsSegment

    NODE_CLASS_MAPPINGS["ImgUtilsSegment"] = ImgUtilsSegment
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsSegment"] = "Imgutils Segment"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsSegment unavailable.", exc_info=True)

try:
    from .node_tagging import ImgUtilsTags

    NODE_CLASS_MAPPINGS["ImgUtilsTags"] = ImgUtilsTags
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsTags"] = "Imgutils Tags"
except Exception:
    logger.warning("imgutils_nodes: ImgUtilsTags unavailable.", exc_info=True)

# Tagging sub-package — 6 tagger nodes
try:
    from .tagging import NODE_CLASS_MAPPINGS as _tagging_cm, NODE_DISPLAY_NAME_MAPPINGS as _tagging_dn

    NODE_CLASS_MAPPINGS.update(_tagging_cm)
    NODE_DISPLAY_NAME_MAPPINGS.update(_tagging_dn)
except Exception:
    logger.warning("imgutils_nodes: Tagging nodes unavailable.", exc_info=True)

# Startup logging
n_nodes = len(NODE_CLASS_MAPPINGS)
logger.info(f"imgutils_nodes v{__version__}: Loaded {n_nodes} nodes.")
if n_nodes == 0:
    logger.warning(
        "imgutils_nodes: No nodes could be loaded. "
        "Check that dghs-imgutils>=0.19.0 is installed."
    )


class ImgUtilsExtension(ComfyExtension):
    """ComfyUI V2 extension entrypoint for imgutils_nodes."""

    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return list(NODE_CLASS_MAPPINGS.values())


async def comfy_entrypoint() -> ImgUtilsExtension:
    """Called by ComfyUI to load this extension."""
    return ImgUtilsExtension()


__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]
