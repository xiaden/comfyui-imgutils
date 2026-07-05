"""imgutils_nodes utility sub-package — bbox, label, dedup, threshold, boolean logic, and JSON filter nodes."""

from .._shared import register_nodes

NODES: list[tuple[str, str, str]] = [
    ("node_bbox", "ImgUtilsBboxUnpack", "Imgutils Bbox Unpack"),
    ("node_bbox_crop", "ImgUtilsBboxCrop", "Imgutils Bbox Crop"),
    ("node_bbox_mask", "ImgUtilsBboxMask", "Imgutils Bbox Mask"),
    ("node_contains", "ImgUtilsLabelContains", "Imgutils Label Contains"),
    ("node_dedup", "ImgUtilsDedup", "Imgutils Deduplicate Tags"),
    ("node_score_threshold", "ImgUtilsScoreThreshold", "Imgutils Score Threshold"),
    ("node_bool_logic", "ImgUtilsBoolLogic", "Imgutils Boolean Logic"),
    ("node_json_filter", "ImgUtilsJSONFilter", "Imgutils JSON Filter"),
]

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes(__name__, NODES)
