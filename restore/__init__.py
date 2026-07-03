"""imgutils_nodes restore sub-package."""
from __future__ import annotations

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .node_scunet import ImgUtilsSCUNet
    NODE_CLASS_MAPPINGS["ImgUtilsSCUNet"] = ImgUtilsSCUNet
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsSCUNet"] = "Imgutils Restore (SCUNet)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsSCUNet unavailable", exc_info=True)

try:
    from .node_nafnet import ImgUtilsNAFNet
    NODE_CLASS_MAPPINGS["ImgUtilsNAFNet"] = ImgUtilsNAFNet
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsNAFNet"] = "Imgutils Restore (NAFNet)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsNAFNet unavailable", exc_info=True)

try:
    from .node_adversarial import ImgUtilsAdversarial
    NODE_CLASS_MAPPINGS["ImgUtilsAdversarial"] = ImgUtilsAdversarial
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsAdversarial"] = "Imgutils Restore (Adversarial)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsAdversarial unavailable", exc_info=True)
