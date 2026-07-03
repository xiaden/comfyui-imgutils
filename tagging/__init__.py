"""imgutils_nodes tagging sub-package — one node per tagger with full knobs."""
from __future__ import annotations

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .node_wd14 import ImgUtilsWD14
    NODE_CLASS_MAPPINGS["ImgUtilsWD14"] = ImgUtilsWD14
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsWD14"] = "Imgutils WD14 Tagger"
except Exception:
    import logging
    logging.getLogger(__name__).warning("ImgUtilsWD14 unavailable", exc_info=True)

try:
    from .node_deepdanbooru import ImgUtilsDeepDanbooru
    NODE_CLASS_MAPPINGS["ImgUtilsDeepDanbooru"] = ImgUtilsDeepDanbooru
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsDeepDanbooru"] = "Imgutils DeepDanbooru Tagger"
except Exception:
    import logging
    logging.getLogger(__name__).warning("ImgUtilsDeepDanbooru unavailable", exc_info=True)

try:
    from .node_deepgelbooru import ImgUtilsDeepGelbooru
    NODE_CLASS_MAPPINGS["ImgUtilsDeepGelbooru"] = ImgUtilsDeepGelbooru
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsDeepGelbooru"] = "Imgutils DeepGelbooru Tagger"
except Exception:
    import logging
    logging.getLogger(__name__).warning("ImgUtilsDeepGelbooru unavailable", exc_info=True)

try:
    from .node_mldanbooru import ImgUtilsMLDanbooru
    NODE_CLASS_MAPPINGS["ImgUtilsMLDanbooru"] = ImgUtilsMLDanbooru
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsMLDanbooru"] = "Imgutils MLDanbooru Tagger"
except Exception:
    import logging
    logging.getLogger(__name__).warning("ImgUtilsMLDanbooru unavailable", exc_info=True)

try:
    from .node_camie import ImgUtilsCamie
    NODE_CLASS_MAPPINGS["ImgUtilsCamie"] = ImgUtilsCamie
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsCamie"] = "Imgutils Camie Tagger"
except Exception:
    import logging
    logging.getLogger(__name__).warning("ImgUtilsCamie unavailable", exc_info=True)

try:
    from .node_pixai import ImgUtilsPixAI
    NODE_CLASS_MAPPINGS["ImgUtilsPixAI"] = ImgUtilsPixAI
    NODE_DISPLAY_NAME_MAPPINGS["ImgUtilsPixAI"] = "Imgutils PixAI Tagger"
except Exception:
    import logging
    logging.getLogger(__name__).warning("ImgUtilsPixAI unavailable", exc_info=True)
