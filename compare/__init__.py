"""imgutils_nodes comparison sub-package — CCIP character similarity and LPIPS perceptual similarity."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_ccip", "ImgUtilsCCIP", "Imgutils Compare (CCIP)"),
    ("node_lpips", "ImgUtilsLPIPS", "Imgutils Compare (LPIPS)"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
