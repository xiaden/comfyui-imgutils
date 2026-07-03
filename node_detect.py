"""
Node 3: ImgUtilsDetect — "Detect things"

Routes a dropdown to imgutils detection functions.
Outputs detection labels/counts and detailed bounding boxes.

Dropdown options (9):
  detect_faces          -> imgutils.detect.detect_faces()
  detect_hands          -> imgutils.detect.detect_hands()
  detect_heads          -> imgutils.detect.detect_heads()
  detect_eyes           -> imgutils.detect.detect_eyes()
  detect_person         -> imgutils.detect.detect_person()
  detect_halfbody       -> imgutils.detect.detect_halfbody()
  detect_with_nudenet   -> imgutils.detect.detect_with_nudenet()
  detect_censors        -> imgutils.detect.detect_censors()
  detect_with_booru_yolo -> imgutils.detect.detect_with_booru_yolo()
"""

from __future__ import annotations

import json
from collections import Counter

from comfy_api.latest import io

from .utils import comfy_to_pil


class ImgUtilsDetect(io.ComfyNode):
    """Detect faces, hands, persons, and other objects using imgutils."""

    DROPDOWN_OPTIONS = [
        "detect_faces",
        "detect_hands",
        "detect_heads",
        "detect_eyes",
        "detect_person",
        "detect_halfbody",
        "detect_with_nudenet",
        "detect_censors",
        "detect_text_with_ocr",
        "detect_with_booru_yolo",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsDetect",
            display_name="Imgutils Detect",
            category="imgutils/detect",
            description=(
                "Detect faces, hands, heads, eyes, persons, half-bodies, "
                "text regions, nude areas, censors, and Booru-tagged objects in anime images."
            ),
            search_aliases=[
                "detect", "detection", "face", "hand", "head", "eye",
                "person", "nudenet", "censor", "booru", "yolo", "bbox",
                "text", "ocr",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to detect objects in"),
                io.Combo.Input(
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="detect_faces",
                    tooltip="Detection type: faces, hands, heads, eyes, persons, half-bodies, nudenet, censors, or Booru YOLO.",
                ),
                io.Float.Input(
                    "confidence",
                    default=0.5,
                    min=0.0,
                    max=1.0,
                    step=0.05,
                    tooltip="Minimum confidence threshold. Detections below this are filtered out.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="detections"),
                io.String.Output(display_name="boxes"),
                io.String.Output(display_name="bboxes"),
            ],
        )

    @classmethod
    def execute(cls, image, operation, confidence) -> io.NodeOutput:
        """
        Run the selected detection and format results.

        Args:
            image: ComfyUI IMAGE tensor (B,H,W,C), float32, [0,1]
            operation: dropdown selection
            confidence: minimum confidence threshold (0.0–1.0)

        Returns:
            NodeOutput with (detections: str, boxes: str)
            - detections: summary of what was found (e.g., "3 faces, 1 hand")
            - boxes: full results with bounding boxes and confidence scores
        """
        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        results = _run_detection(pil_image, operation, float(confidence))
        detections_str, boxes_str = _format_detection_results(results, confidence)
        bboxes_json = json.dumps([
            {"bbox": [bbox[0], bbox[1], bbox[2], bbox[3]], "label": label, "confidence": conf}
            for bbox, label, conf in results
        ], ensure_ascii=False)
        return io.NodeOutput(detections_str, boxes_str, bboxes_json)


def _run_detection(pil_image, operation: str, confidence: float) -> list:
    """Run a detection function and return raw results."""
    import importlib

    detect_map = {
        "detect_faces": "imgutils.detect.detect_faces",
        "detect_hands": "imgutils.detect.detect_hands",
        "detect_heads": "imgutils.detect.detect_heads",
        "detect_eyes": "imgutils.detect.detect_eyes",
        "detect_person": "imgutils.detect.detect_person",
        "detect_halfbody": "imgutils.detect.detect_halfbody",
        "detect_with_nudenet": "imgutils.detect.detect_with_nudenet",
        "detect_censors": "imgutils.detect.detect_censors",
        "detect_text_with_ocr": "imgutils.ocr.detect_text_with_ocr",
        "detect_with_booru_yolo": "imgutils.detect.detect_with_booru_yolo",
    }

    module_name, func_name = detect_map[operation].rsplit(".", 1)
    mod = importlib.import_module(module_name)
    raw = getattr(mod, func_name)(pil_image)

    # Filter by confidence threshold
    filtered = []
    for item in raw:
        bbox, label, conf = item
        if conf >= confidence:
            filtered.append(item)

    return filtered


def _format_detection_results(results: list, confidence: float) -> tuple[str, str]:
    """
    Format detection results as (detections_summary, boxes_detail).

    detections: count by label, e.g. "face: 3, hand: 1"
    boxes: each detection with bbox, label, and confidence
    """
    if not results:
        return (
            f"No detections at confidence >= {confidence:.2f}",
            f"No detections at confidence >= {confidence:.2f}",
        )

    # Count by label for summary
    counts = Counter(label for bbox, label, conf in results)
    detections_str = ", ".join(f"{label}: {count}" for label, count in sorted(counts.items()))

    # Full box details
    lines = [f"=== Detections (confidence >= {confidence:.2f}, {len(results)} found) ===", ""]
    for bbox, label, conf in sorted(results, key=lambda x: x[2], reverse=True):
        x1, y1, x2, y2 = bbox
        lines.append(f"  [{x1},{y1},{x2},{y2}] {label} ({conf:.4f})")

    return (detections_str, "\n".join(lines))
