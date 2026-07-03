"""imgutils_nodes compare sub-package."""
from __future__ import annotations

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .node_ccip import ImgUtilsCCIP
    NODE_CLASS_MAPPINGS["ImgUtilsCCIP"] = ImgUtilsCCIP
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCCIP"] = "Imgutils Compare (CCIP)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsCCIP unavailable", exc_info=True)

try:
    from .node_lpips import ImgUtilsLPIPS
    NODE_CLASS_MAPPINGS["ImgUtilsLPIPS"] = ImgUtilsLPIPS
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsLPIPS"] = "Imgutils Compare (LPIPS)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsLPIPS unavailable", exc_info=True)
