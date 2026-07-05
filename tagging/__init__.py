"""imgutils_nodes tagging sub-package — taggers and tag-string processing."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_wd14", "ImgUtilsWD14", "Imgutils WD14 Tagger"),
    ("node_deepdanbooru", "ImgUtilsDeepDanbooru", "Imgutils DeepDanbooru Tagger"),
    ("node_deepgelbooru", "ImgUtilsDeepGelbooru", "Imgutils DeepGelbooru Tagger"),
    ("node_mldanbooru", "ImgUtilsMLDanbooru", "Imgutils MLDanbooru Tagger"),
    ("node_camie", "ImgUtilsCamie", "Imgutils Camie Tagger"),
    ("node_pixai", "ImgUtilsPixAI", "Imgutils PixAI Tagger"),
    ("node_tags", "ImgUtilsTags", "Imgutils Tags"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
