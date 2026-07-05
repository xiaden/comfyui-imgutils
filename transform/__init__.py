"""imgutils_nodes transform sub-package — CDC upscaling, censoring, alignment, and squeeze-crop."""

from .node_cdc import ImgUtilsCDC
from .node_censor import ImgUtilsCensor
from .node_align import ImgUtilsAlign
from .node_squeeze import ImgUtilsSqueeze

NODE_CLASSES = [ImgUtilsCDC, ImgUtilsCensor, ImgUtilsAlign, ImgUtilsSqueeze]
