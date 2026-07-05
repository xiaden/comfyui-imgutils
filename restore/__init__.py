"""imgutils_nodes restore sub-package — SCUNet, NAFNet, and adversarial noise removal."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_scunet", "ImgUtilsSCUNet", "Imgutils Restore (SCUNet)"),
    ("node_nafnet", "ImgUtilsNAFNet", "Imgutils Restore (NAFNet)"),
    ("node_adversarial", "ImgUtilsAdversarial", "Imgutils Restore (Adversarial)"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
