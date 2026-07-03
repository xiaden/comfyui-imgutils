"""
Node: ImgUtilsBboxUnpack — "Unpack bboxes"

Takes a raw bbox string from any imgutils detection/OCR function
and unpacks it into count, labels, and an iterable JSON array.
"""

from __future__ import annotations

import json
import re
from typing import Any

from comfy_api.latest import io


def _parse_bboxes(text: str) -> list[dict[str, Any]]:
    """
    Parse a bbox result string into a list of structured entries.

    Accepts these formats (preference order):

    1. JSON array (ImgUtilsOCR/ImgUtilsDetect "bboxes" output):
       [{"bbox": [x1,y1,x2,y2], "label": "...", "score": 0.95}, ...]

    2. Detection text (ImgUtilsDetect "boxes" output):
       [x1,y1,x2,y2] label (0.9500)

    3. OCR text (ImgUtilsOCR "scores" output):
       [x1,y1,x2,y2] "text" (0.9500)
    """
    text = text.strip()

    # ---- 1. JSON format ----
    if text.startswith("[") and text.endswith("]"):
        try:
            raw = json.loads(text)
        except json.JSONDecodeError:
            pass
        else:
            entries: list[dict[str, Any]] = []
            for item in raw:
                if not isinstance(item, dict):
                    continue
                bbox = item.get("bbox") or item.get("box") or item.get("coords", [0, 0, 0, 0])
                if isinstance(bbox, list) and len(bbox) == 4:
                    entries.append({
                        "x1": int(bbox[0]), "y1": int(bbox[1]),
                        "x2": int(bbox[2]), "y2": int(bbox[3]),
                        "label": str(item["label"]),
                        "score": float(item["score"]),
                    })
            if entries:
                return entries

    # ---- 2. Detection format: "[x1,y1,x2,y2] label (0.9500)" ----
    detect_pattern = re.compile(
        r"\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\s+"
        r"(\S+?)\s*\(\s*([\d.]+)\s*\)"
    )
    detect_matches = detect_pattern.findall(text)
    if detect_matches:
        return [
            {
                "x1": int(x1), "y1": int(y1),
                "x2": int(x2), "y2": int(y2),
                "label": label,
                "score": float(score),
            }
            for x1, y1, x2, y2, label, score in detect_matches
        ]

    # ---- 3. OCR format: '[x1,y1,x2,y2] "text" (0.9500)' ----
    ocr_pattern = re.compile(
        r"\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\s+"
        r"[\"']([^\"']+)[\"']\s*\(\s*([\d.]+)\s*\)"
    )
    ocr_matches = ocr_pattern.findall(text)
    if ocr_matches:
        return [
            {
                "x1": int(x1), "y1": int(y1),
                "x2": int(x2), "y2": int(y2),
                "label": label,
                "score": float(score),
            }
            for x1, y1, x2, y2, label, score in ocr_matches
        ]

    return []


class ImgUtilsBboxUnpack(io.ComfyNode):
    """Unpack bbox output from imgutils nodes into count, labels, and iterable JSON."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsBboxUnpack",
            display_name="Imgutils Bbox Unpack",
            category="imgutils/bbox",
            description=(
                "Unpack a raw bbox result string from imgutils OCR or detection nodes "
                "into a count, comma-separated labels, and an iterable JSON array "
                "suitable for use with forLoopStart/ForeachListBegin iterators."
            ),
            inputs=[
                io.String.Input(
                    "bbox_string",
                    tooltip="Raw bbox output from imgutils nodes (JSON array or text-tuple format).",
                ),
            ],
            outputs=[
                io.Int.Output(display_name="count"),
                io.String.Output(display_name="labels"),
                io.String.Output(display_name="iterable"),
            ],
        )

    @classmethod
    def execute(cls, bbox_string) -> io.NodeOutput:
        """
        Parse bbox string and emit structured outputs.

        Args:
            bbox_string: Raw result string from an imgutils function.

        Returns:
            NodeOutput with (count: int, labels: str, iterable: str)
        """
        entries = _parse_bboxes(bbox_string)

        count = len(entries)

        labels = ", ".join(e["label"] for e in entries) if entries else ""

        iterable = json.dumps(
            [
                {
                    "x1": e["x1"], "y1": e["y1"],
                    "x2": e["x2"], "y2": e["y2"],
                    "label": e["label"],
                    "score": e["score"],
                    "width": e["x2"] - e["x1"],
                    "height": e["y2"] - e["y1"],
                }
                for e in entries
            ],
            ensure_ascii=False,
        )

        return io.NodeOutput(count, labels, iterable)
