"""imgutils_nodes edge detection sub-package."""
from __future__ import annotations

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .node_canny import ImgUtilsCanny
    NODE_CLASS_MAPPINGS["ImgUtilsCanny"] = ImgUtilsCanny
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCanny"] = "Imgutils Edge (Canny)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsCanny unavailable", exc_info=True)

try:
    from .node_lineart import ImgUtilsLineart
    NODE_CLASS_MAPPINGS["ImgUtilsLineart"] = ImgUtilsLineart
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsLineart"] = "Imgutils Edge (Lineart)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsLineart unavailable", exc_info=True)

try:
    from .node_lineart_anime import ImgUtilsLineartAnime
    NODE_CLASS_MAPPINGS["ImgUtilsLineartAnime"] = ImgUtilsLineartAnime
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsLineartAnime"] = "Imgutils Edge (Lineart Anime)"
except Exception:
    import logging; logging.getLogger(__name__).warning("ImgUtilsLineartAnime unavailable", exc_info=True)
