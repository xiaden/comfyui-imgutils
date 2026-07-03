"""
imgutils_nodes — ComfyUI custom node pack wrapping deepghs/imgutils.

Provides 26 nodes for anime image analysis, tagging, detection, and processing.
Uses the ComfyUI V2 io.ComfyNode API.
"""

from __future__ import annotations

import logging

from comfy_api.latest import ComfyExtension, io

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


def _merge(prefix: str, cm: dict, dn: dict):
    """Merge NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS from a sub-package."""
    NODE_CLASS_MAPPINGS.update(cm)
    NODE_DISPLAY_NAME_MAPPINGS.update(dn)


# --- Root nodes ---

try:
    from .node_ocr import ImgUtilsOCR
    NODE_CLASS_MAPPINGS["ImgUtilsOCR"] = ImgUtilsOCR
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsOCR"] = "Imgutils OCR"
except Exception:
    logger.warning("ImgUtilsOCR unavailable.", exc_info=True)

try:
    from .node_detect import ImgUtilsDetect
    NODE_CLASS_MAPPINGS["ImgUtilsDetect"] = ImgUtilsDetect
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsDetect"] = "Imgutils Detect"
except Exception:
    logger.warning("ImgUtilsDetect unavailable.", exc_info=True)

try:
    from .node_pose import ImgUtilsPose
    NODE_CLASS_MAPPINGS["ImgUtilsPose"] = ImgUtilsPose
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsPose"] = "Imgutils Pose"
except Exception:
    logger.warning("ImgUtilsPose unavailable.", exc_info=True)

try:
    from .node_segment import ImgUtilsSegment
    NODE_CLASS_MAPPINGS["ImgUtilsSegment"] = ImgUtilsSegment
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsSegment"] = "Imgutils Segment"
except Exception:
    logger.warning("ImgUtilsSegment unavailable.", exc_info=True)

try:
    from .node_tagging import ImgUtilsTags
    NODE_CLASS_MAPPINGS["ImgUtilsTags"] = ImgUtilsTags
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsTags"] = "Imgutils Tags"
except Exception:
    logger.warning("ImgUtilsTags unavailable.", exc_info=True)

try:
    from .node_cdc import ImgUtilsCDC
    NODE_CLASS_MAPPINGS["ImgUtilsCDC"] = ImgUtilsCDC
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCDC"] = "Imgutils Upscale (CDC)"
except Exception:
    logger.warning("ImgUtilsCDC unavailable.", exc_info=True)

try:
    from .node_censor import ImgUtilsCensor
    NODE_CLASS_MAPPINGS["ImgUtilsCensor"] = ImgUtilsCensor
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCensor"] = "Imgutils Censor"
except Exception:
    logger.warning("ImgUtilsCensor unavailable.", exc_info=True)

try:
    from .node_align import ImgUtilsAlign
    NODE_CLASS_MAPPINGS["ImgUtilsAlign"] = ImgUtilsAlign
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsAlign"] = "Imgutils Align"
except Exception:
    logger.warning("ImgUtilsAlign unavailable.", exc_info=True)

try:
    from .node_squeeze import ImgUtilsSqueeze
    NODE_CLASS_MAPPINGS["ImgUtilsSqueeze"] = ImgUtilsSqueeze
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsSqueeze"] = "Imgutils Squeeze"
except Exception:
    logger.warning("ImgUtilsSqueeze unavailable.", exc_info=True)

try:
    from .node_bbox import ImgUtilsBboxUnpack
    NODE_CLASS_MAPPINGS["ImgUtilsBboxUnpack"] = ImgUtilsBboxUnpack
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsBboxUnpack"] = "Imgutils Bbox Unpack"
except Exception:
    logger.warning("ImgUtilsBboxUnpack unavailable.", exc_info=True)

# --- Sub-packages ---

try:
    from .tagging import NODE_CLASS_MAPPINGS as _cm, NODE_DISPLAY_NAME_MAPPINGS as _dn
    _merge("tagging", _cm, _dn)
except Exception:
    logger.warning("Tagging nodes unavailable.", exc_info=True)

try:
    from .edge import NODE_CLASS_MAPPINGS as _cm, NODE_DISPLAY_NAME_MAPPINGS as _dn
    _merge("edge", _cm, _dn)
except Exception:
    logger.warning("Edge nodes unavailable.", exc_info=True)

try:
    from .restore import NODE_CLASS_MAPPINGS as _cm, NODE_DISPLAY_NAME_MAPPINGS as _dn
    _merge("restore", _cm, _dn)
except Exception:
    logger.warning("Restore nodes unavailable.", exc_info=True)

try:
    from .compare import NODE_CLASS_MAPPINGS as _cm, NODE_DISPLAY_NAME_MAPPINGS as _dn
    _merge("compare", _cm, _dn)
except Exception:
    logger.warning("Compare nodes unavailable.", exc_info=True)

try:
    from .judge import NODE_CLASS_MAPPINGS as _cm, NODE_DISPLAY_NAME_MAPPINGS as _dn
    _merge("judge", _cm, _dn)
except Exception:
    logger.warning("Judge nodes unavailable.", exc_info=True)

# --- Startup ---

n_nodes = len(NODE_CLASS_MAPPINGS)
logger.info(f"imgutils_nodes v{__version__}: Loaded {n_nodes} nodes.")
if n_nodes == 0:
    logger.warning("imgutils_nodes: No nodes loaded. Check dghs-imgutils>=0.19.0.")


class ImgUtilsExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return list(NODE_CLASS_MAPPINGS.values())


async def comfy_entrypoint() -> ImgUtilsExtension:
    return ImgUtilsExtension()


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
