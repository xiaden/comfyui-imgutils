"""imgutils_nodes edge detection sub-package — Canny, Lineart, and Anime Lineart."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_canny", "ImgUtilsCanny", "Imgutils Edge (Canny)"),
    ("node_lineart", "ImgUtilsLineart", "Imgutils Edge (Lineart)"),
    ("node_lineart_anime", "ImgUtilsLineartAnime", "Imgutils Edge (Lineart Anime)"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
