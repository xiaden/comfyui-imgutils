"""imgutils_nodes pose sub-package — human keypoint detection and skeleton rendering."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_pose", "ImgUtilsPose", "Imgutils Pose"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
