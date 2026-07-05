"""
imgutils_nodes — ComfyUI custom node pack wrapping deepghs/imgutils.

Provides 34 nodes for anime image analysis, tagging, detection, and processing.
Uses the ComfyUI V3 io.ComfyNode API.
"""

import logging

from comfy_api.latest import ComfyExtension, io

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

# Pure V3 extension — no NODE_CLASS_MAPPINGS at module level.
# Node classes are collected at import time into an internal list
# and served through the ComfyExtension interface.

_SUB_PACKAGES: list[str] = [
    "tagging", "detect", "pose", "segment",
    "edge", "restore", "compare", "judge",
    "transform", "utility",
]

_NODE_CLASSES: list[type[io.ComfyNode]] = []


def _register_subpackage(pkg: str) -> None:
    """Import a subpackage and collect its node classes into the extension list."""
    try:
        mod = __import__(
            f"{__name__}.{pkg}",
            fromlist=["NODE_CLASS_MAPPINGS"],
        )
        _NODE_CLASSES.extend(mod.NODE_CLASS_MAPPINGS.values())
    except Exception:
        logger.warning(f"{pkg.title()} nodes unavailable.", exc_info=True)


for _pkg in _SUB_PACKAGES:
    _register_subpackage(_pkg)

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
