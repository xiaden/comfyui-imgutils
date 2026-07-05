"""imgutils_nodes comparison sub-package — CCIP character similarity and LPIPS perceptual similarity."""

from .node_ccip import ImgUtilsCCIP
from .node_lpips import ImgUtilsLPIPS

NODE_CLASSES = [ImgUtilsCCIP, ImgUtilsLPIPS]
