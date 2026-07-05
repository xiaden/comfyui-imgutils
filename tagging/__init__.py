"""imgutils_nodes tagging sub-package — taggers and tag-string processing."""

from .node_wd14 import ImgUtilsWD14
from .node_deepdanbooru import ImgUtilsDeepDanbooru
from .node_deepgelbooru import ImgUtilsDeepGelbooru
from .node_mldanbooru import ImgUtilsMLDanbooru
from .node_camie import ImgUtilsCamie
from .node_pixai import ImgUtilsPixAI
from .node_tags import ImgUtilsTags

NODE_CLASSES = [
    ImgUtilsWD14, ImgUtilsDeepDanbooru, ImgUtilsDeepGelbooru,
    ImgUtilsMLDanbooru, ImgUtilsCamie, ImgUtilsPixAI, ImgUtilsTags,
]
