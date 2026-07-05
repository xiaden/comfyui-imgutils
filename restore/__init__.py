"""imgutils_nodes restore sub-package — SCUNet, NAFNet, and adversarial noise removal."""

from .node_scunet import ImgUtilsSCUNet
from .node_nafnet import ImgUtilsNAFNet
from .node_adversarial import ImgUtilsAdversarial

NODE_CLASSES = [ImgUtilsSCUNet, ImgUtilsNAFNet, ImgUtilsAdversarial]
