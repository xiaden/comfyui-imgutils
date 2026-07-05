"""imgutils_nodes edge detection sub-package — Canny, Lineart, and Anime Lineart."""

from .node_canny import ImgUtilsCanny
from .node_lineart import ImgUtilsLineart
from .node_lineart_anime import ImgUtilsLineartAnime

NODE_CLASSES = [ImgUtilsCanny, ImgUtilsLineart, ImgUtilsLineartAnime]
