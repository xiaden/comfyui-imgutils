"""
imgutils_nodes — ComfyUI custom node pack wrapping deepghs/imgutils.

Provides 34 nodes for anime image analysis, tagging, detection, and processing.
Uses the ComfyUI V3 io.ComfyNode API.
"""

import logging

from comfy_api.latest import ComfyExtension, io

from .compare.node_ccip import ImgUtilsCCIP
from .compare.node_lpips import ImgUtilsLPIPS
from .detect.node_detect import ImgUtilsDetect
from .detect.node_ocr import ImgUtilsOCR
from .edge.node_canny import ImgUtilsCanny
from .edge.node_lineart import ImgUtilsLineart
from .edge.node_lineart_anime import ImgUtilsLineartAnime
from .judge.node_classify import ImgUtilsClassify
from .judge.node_check import ImgUtilsCheck
from .judge.node_metric import ImgUtilsMetric
from .pose.node_pose import ImgUtilsPose
from .restore.node_scunet import ImgUtilsSCUNet
from .restore.node_nafnet import ImgUtilsNAFNet
from .restore.node_adversarial import ImgUtilsAdversarial
from .segment.node_segment import ImgUtilsSegment
from .tagging.node_wd14 import ImgUtilsWD14
from .tagging.node_deepdanbooru import ImgUtilsDeepDanbooru
from .tagging.node_deepgelbooru import ImgUtilsDeepGelbooru
from .tagging.node_mldanbooru import ImgUtilsMLDanbooru
from .tagging.node_camie import ImgUtilsCamie
from .tagging.node_pixai import ImgUtilsPixAI
from .tagging.node_tags import ImgUtilsTags
from .transform.node_cdc import ImgUtilsCDC
from .transform.node_censor import ImgUtilsCensor
from .transform.node_align import ImgUtilsAlign
from .transform.node_squeeze import ImgUtilsSqueeze
from .utility.node_bbox import ImgUtilsBboxUnpack
from .utility.node_bbox_crop import ImgUtilsBboxCrop
from .utility.node_bbox_mask import ImgUtilsBboxMask
from .utility.node_contains import ImgUtilsLabelContains
from .utility.node_dedup import ImgUtilsDedup
from .utility.node_score_threshold import ImgUtilsScoreThreshold
from .utility.node_bool_logic import ImgUtilsBoolLogic
from .utility.node_json_filter import ImgUtilsJSONFilter

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

_NODE_CLASSES: list[type[io.ComfyNode]] = [
    ImgUtilsCCIP, ImgUtilsLPIPS,
    ImgUtilsDetect, ImgUtilsOCR,
    ImgUtilsCanny, ImgUtilsLineart, ImgUtilsLineartAnime,
    ImgUtilsClassify, ImgUtilsCheck, ImgUtilsMetric,
    ImgUtilsPose,
    ImgUtilsSCUNet, ImgUtilsNAFNet, ImgUtilsAdversarial,
    ImgUtilsSegment,
    ImgUtilsWD14, ImgUtilsDeepDanbooru, ImgUtilsDeepGelbooru,
    ImgUtilsMLDanbooru, ImgUtilsCamie, ImgUtilsPixAI, ImgUtilsTags,
    ImgUtilsCDC, ImgUtilsCensor, ImgUtilsAlign, ImgUtilsSqueeze,
    ImgUtilsBboxUnpack, ImgUtilsBboxCrop, ImgUtilsBboxMask,
    ImgUtilsLabelContains, ImgUtilsDedup, ImgUtilsScoreThreshold,
    ImgUtilsBoolLogic, ImgUtilsJSONFilter,
]

n_nodes = len(_NODE_CLASSES)
logger.info(f"imgutils_nodes v{__version__}: Loaded {n_nodes} nodes.")
if n_nodes == 0:
    logger.warning("imgutils_nodes: No nodes loaded. Check dghs-imgutils>=0.19.0.")


class ImgUtilsExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            ImgUtilsCCIP, ImgUtilsLPIPS,
            ImgUtilsDetect, ImgUtilsOCR,
            ImgUtilsCanny, ImgUtilsLineart, ImgUtilsLineartAnime,
            ImgUtilsClassify, ImgUtilsCheck, ImgUtilsMetric,
            ImgUtilsPose,
            ImgUtilsSCUNet, ImgUtilsNAFNet, ImgUtilsAdversarial,
            ImgUtilsSegment,
            ImgUtilsWD14, ImgUtilsDeepDanbooru, ImgUtilsDeepGelbooru,
            ImgUtilsMLDanbooru, ImgUtilsCamie, ImgUtilsPixAI, ImgUtilsTags,
            ImgUtilsCDC, ImgUtilsCensor, ImgUtilsAlign, ImgUtilsSqueeze,
            ImgUtilsBboxUnpack, ImgUtilsBboxCrop, ImgUtilsBboxMask,
            ImgUtilsLabelContains, ImgUtilsDedup, ImgUtilsScoreThreshold,
            ImgUtilsBoolLogic, ImgUtilsJSONFilter,
        ]


async def comfy_entrypoint() -> ImgUtilsExtension:
    return ImgUtilsExtension()


__all__ = ["comfy_entrypoint"]
