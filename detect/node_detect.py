"""Object detection for anime images — faces, hands, persons, nudity, text, and YOLO-tagged objects."""

import importlib
import json
from collections import Counter

from comfy_api.latest import io

from .._shared.tensor import comfy_to_pil
from .._shared.formatting import label_display


class ImgUtilsDetect(io.ComfyNode):
    """Detect faces, hands, bodies, nudity, text, and Booru objects in anime images."""

    DROPDOWN_OPTIONS = [
        "Detect Faces",
        "Detect Hands",
        "Detect Heads",
        "Detect Eyes",
        "Detect Person",
        "Detect Halfbody",
        "Detect with NudeNet",
        "Detect Censors",
        "Detect Text with OCR",
        "Detect with Booru YOLO",
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
                io.Image.Input("image", tooltip="Input image for object detection."),
                io.Combo.Input(
                    "mode",
                    options=cls.DROPDOWN_OPTIONS,
                    default="Detect Faces",
                    tooltip="What to detect — faces, hands, heads, eyes, persons, nudity, censors, text, or Booru YOLO objects.",
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
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, mode, confidence) -> io.NodeOutput:
        pil_image = comfy_to_pil(image)
        results = _run_detection(pil_image, mode, confidence)

        if not results:
            return io.NodeOutput(
                f"No detections at confidence >= {confidence:.2f}",
                "[]",
            )

        counts = Counter(label for bbox, label, conf in results)
        detections_str = ", ".join(
            f"{label_display(label)}: {count}" for label, count in sorted(counts.items())
        )
        bboxes_json = json.dumps([
            {"bbox": [bbox[0], bbox[1], bbox[2], bbox[3]], "label": label_display(label), "score": conf}
            for bbox, label, conf in results
        ], ensure_ascii=False)
        return io.NodeOutput(detections_str, bboxes_json)


def _run_detection(pil_image, mode: str, confidence: float) -> list[tuple]:
    """Run a detection function and return raw results."""
    detect_map = {
        "Detect Faces": "imgutils.detect.detect_faces",
        "Detect Hands": "imgutils.detect.detect_hands",
        "Detect Heads": "imgutils.detect.detect_heads",
        "Detect Eyes": "imgutils.detect.detect_eyes",
        "Detect Person": "imgutils.detect.detect_person",
        "Detect Halfbody": "imgutils.detect.detect_halfbody",
        "Detect with NudeNet": "imgutils.detect.detect_with_nudenet",
        "Detect Censors": "imgutils.detect.detect_censors",
        "Detect Text with OCR": "imgutils.ocr.detect_text_with_ocr",
        "Detect with Booru YOLO": "imgutils.detect.detect_with_booru_yolo",
    }

    module_name, func_name = detect_map[mode].rsplit(".", 1)
    mod = importlib.import_module(module_name)
    raw = getattr(mod, func_name)(pil_image)

    filtered = []
    for item in raw:
        bbox, label, conf = item
        if conf >= confidence:
            filtered.append(item)

    return filtered
