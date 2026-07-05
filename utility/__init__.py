"""imgutils_nodes utility sub-package — bbox, label, dedup, threshold, boolean logic, and JSON filter nodes."""

from .node_bbox import ImgUtilsBboxUnpack
from .node_bbox_crop import ImgUtilsBboxCrop
from .node_bbox_mask import ImgUtilsBboxMask
from .node_contains import ImgUtilsLabelContains
from .node_dedup import ImgUtilsDedup
from .node_score_threshold import ImgUtilsScoreThreshold
from .node_bool_logic import ImgUtilsBoolLogic
from .node_json_filter import ImgUtilsJSONFilter

NODE_CLASSES = [
    ImgUtilsBboxUnpack, ImgUtilsBboxCrop, ImgUtilsBboxMask,
    ImgUtilsLabelContains, ImgUtilsDedup, ImgUtilsScoreThreshold,
    ImgUtilsBoolLogic, ImgUtilsJSONFilter,
]
