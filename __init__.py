"""
imgutils_nodes — ComfyUI custom node pack wrapping deepghs/imgutils.

Provides 34 nodes for anime image analysis, tagging, detection, and processing.
Uses the ComfyUI V3 io.ComfyNode API.
"""

import logging

from comfy_api.latest import ComfyExtension, io

from .compare import NODE_CLASSES as _compare_nodes
from .detect import NODE_CLASSES as _detect_nodes
from .edge import NODE_CLASSES as _edge_nodes
from .judge import NODE_CLASSES as _judge_nodes
from .pose import NODE_CLASSES as _pose_nodes
from .restore import NODE_CLASSES as _restore_nodes
from .segment import NODE_CLASSES as _segment_nodes
from .tagging import NODE_CLASSES as _tagging_nodes
from .transform import NODE_CLASSES as _transform_nodes
from .utility import NODE_CLASSES as _utility_nodes

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

_NODE_CLASSES: list[type[io.ComfyNode]] = (
    _compare_nodes + _detect_nodes + _edge_nodes + _judge_nodes
    + _pose_nodes + _restore_nodes + _segment_nodes + _tagging_nodes
    + _transform_nodes + _utility_nodes
)

n_nodes = len(_NODE_CLASSES)
logger.info(f"imgutils_nodes v{__version__}: Loaded {n_nodes} nodes.")
if n_nodes == 0:
    logger.warning("imgutils_nodes: No nodes loaded. Check dghs-imgutils>=0.19.0.")


class ImgUtilsExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return list(_NODE_CLASSES)


async def comfy_entrypoint() -> ImgUtilsExtension:
    return ImgUtilsExtension()


__all__ = ["comfy_entrypoint"]
