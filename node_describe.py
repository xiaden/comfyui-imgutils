"""
Node 2: ImgUtilsDescribe — "Describe this"

Routes a dropdown to imgutils tagging, OCR, and detection functions.
Outputs structured text describing the image.

Dropdown options (17):
  Tagging (output rating/features/characters as structured text):
    get_wd14_tags         -> imgutils.tagging.wd14.get_wd14_tags()
    get_deepdanbooru_tags -> imgutils.tagging.deepdanbooru.get_deepdanbooru_tags()
    get_mldanbooru_tags   -> imgutils.tagging.mldanbooru.get_mldanbooru_tags()
    camie_tags            -> imgutils.tagging.camie.get_camie_tags()
    deepgelbooru_tags     -> imgutils.tagging.deepgelbooru.get_deepgelbooru_tags()
    pixai_tags            -> imgutils.tagging.pixai.get_pixai_tags()

  OCR (output recognized text with bounding boxes):
    ocr                   -> imgutils.ocr.ocr()
    detect_text_with_ocr  -> imgutils.ocr.detect_text_with_ocr() [bboxes only, no text recognition]

  Detection (output bounding boxes as text):
    detect_faces          -> imgutils.detect.face.detect_faces()
    detect_hands          -> imgutils.detect.hand.detect_hands()
    detect_heads          -> imgutils.detect.head.detect_heads()
    detect_eyes           -> imgutils.detect.eye.detect_eyes()
    detect_person         -> imgutils.detect.person.detect_person()
    detect_halfbody       -> imgutils.detect.halfbody.detect_halfbody()
    detect_with_nudenet   -> imgutils.detect.nudenet.detect_with_nudenet()
    detect_censors        -> imgutils.detect.censor.detect_censors()
    detect_with_booru_yolo -> imgutils.detect.booru_yolo.detect_with_booru_yolo()
"""

from __future__ import annotations

from comfy_api.latest import io

from .utils import comfy_to_pil


class ImgUtilsDescribe(io.ComfyNode):
    """Describe an image using imgutils tagging, OCR, and detection."""

    DROPDOWN_OPTIONS = [
        "get_wd14_tags",
        "get_deepdanbooru_tags",
        "get_mldanbooru_tags",
        "camie_tags",
        "deepgelbooru_tags",
        "pixai_tags",
        "ocr",
        "detect_text_with_ocr",
        "detect_faces",
        "detect_hands",
        "detect_heads",
        "detect_eyes",
        "detect_person",
        "detect_halfbody",
        "detect_with_nudenet",
        "detect_censors",
        "detect_with_booru_yolo",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsDescribe",
            display_name="Imgutils Describe",
            category="imgutils/describe",
            description=(
                "Analyze and describe anime images — WD14/DeepDanbooru/MLDanbooru/Camie/PixAI "
                "tagging, OCR text detection, and face/hand/eye/person/censor detection."
            ),
            search_aliases=[
                "describe", "tagging", "wd14", "deepdanbooru", "mldanbooru",
                "camie", "pixai", "ocr", "detect", "face", "hand", "eye",
                "person", "censor", "booru",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to analyze"),
                io.Combo.Input(
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="get_wd14_tags",
                    tooltip="Select analysis operation: WD14/DeepDanbooru tagging, OCR, or detection (faces, hands, eyes, persons, etc.)",
                ),
            ],
            outputs=[
                io.String.Output(display_name="text"),
            ],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        """
        Route the operation to the correct imgutils function and format output.

        Args:
            image: ComfyUI IMAGE tensor (B,H,W,C), float32, [0,1]
            operation: dropdown selection

        Returns:
            NodeOutput with (text_string,)
        """
        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        # ---- Tagging functions ----
        if operation == "get_wd14_tags":
            from imgutils.tagging import get_wd14_tags

            rating, general, character = get_wd14_tags(pil_image)
            return io.NodeOutput(_format_wd14_tags(rating, general, character))

        elif operation == "get_deepdanbooru_tags":
            from imgutils.tagging import get_deepdanbooru_tags

            result = get_deepdanbooru_tags(pil_image)
            return io.NodeOutput(_format_tag_dict(result, "DeepDanbooru Tags"))

        elif operation == "get_mldanbooru_tags":
            from imgutils.tagging import get_mldanbooru_tags

            result = get_mldanbooru_tags(pil_image)
            return io.NodeOutput(_format_tag_dict(result, "MLDanbooru Tags"))

        elif operation == "camie_tags":
            from imgutils.tagging import get_camie_tags

            result = get_camie_tags(pil_image)
            return io.NodeOutput(_format_tag_dict(result, "Camie Tags"))

        elif operation == "deepgelbooru_tags":
            from imgutils.tagging import get_deepgelbooru_tags

            result = get_deepgelbooru_tags(pil_image)
            return io.NodeOutput(_format_tag_dict(result, "DeepGelbooru Tags"))

        elif operation == "pixai_tags":
            from imgutils.tagging import get_pixai_tags

            result = get_pixai_tags(pil_image)
            return io.NodeOutput(_format_tag_dict(result, "PixAI Tags"))

        # ---- OCR functions ----
        elif operation == "ocr":
            from imgutils.ocr import ocr

            results = ocr(pil_image)
            return io.NodeOutput(_format_ocr_results(results, include_text=True))

        elif operation == "detect_text_with_ocr":
            from imgutils.ocr import detect_text_with_ocr

            results = detect_text_with_ocr(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Text Regions"))

        # ---- Detection functions ----
        elif operation == "detect_faces":
            from imgutils.detect import detect_faces

            results = detect_faces(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Faces"))

        elif operation == "detect_hands":
            from imgutils.detect import detect_hands

            results = detect_hands(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Hands"))

        elif operation == "detect_heads":
            from imgutils.detect import detect_heads

            results = detect_heads(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Heads"))

        elif operation == "detect_eyes":
            from imgutils.detect import detect_eyes

            results = detect_eyes(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Eyes"))

        elif operation == "detect_person":
            from imgutils.detect import detect_person

            results = detect_person(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Persons"))

        elif operation == "detect_halfbody":
            from imgutils.detect import detect_halfbody

            results = detect_halfbody(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Half-bodies"))

        elif operation == "detect_with_nudenet":
            from imgutils.detect import detect_with_nudenet

            results = detect_with_nudenet(pil_image)
            return io.NodeOutput(_format_detection_results(results, "NudeNet Detection"))

        elif operation == "detect_censors":
            from imgutils.detect import detect_censors

            results = detect_censors(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Censors"))

        elif operation == "detect_with_booru_yolo":
            from imgutils.detect import detect_with_booru_yolo

            results = detect_with_booru_yolo(pil_image)
            return io.NodeOutput(_format_detection_results(results, "Booru YOLO"))

        else:
            return io.NodeOutput(f"Unknown operation: {operation}")


def _format_wd14_tags(rating: dict, general: dict, character: dict) -> str:
    """Format WD14 tagger output as structured text."""
    lines = ["=== WD14 Tags ===", ""]
    lines.append("## Rating")
    for k, v in sorted(rating.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {k}: {v:.4f}")
    lines.append("")
    lines.append(f"## General Tags ({len(general)} items)")
    for k, v in sorted(general.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {k}: {v:.4f}")
    lines.append("")
    lines.append(f"## Characters ({len(character)} items)")
    for k, v in sorted(character.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {k}: {v:.4f}")
    return "\n".join(lines)


def _format_tag_dict(tags: dict, title: str) -> str:
    """Format a flat tag dict as structured text."""
    lines = [f"=== {title} ===", ""]
    if isinstance(tags, dict):
        for k, v in sorted(tags.items(), key=lambda x: x[1], reverse=True):  # type: ignore[arg-type]  # mypy can't resolve generic key type for sorted lambda
            if isinstance(v, float):
                lines.append(f"  {k}: {v:.4f}")
            else:
                lines.append(f"  {k}: {v}")
    else:
        lines.append(str(tags))
    return "\n".join(lines)


def _format_ocr_results(results: list, include_text: bool = True) -> str:
    """
    Format OCR results as text.

    OCR results are List[Tuple[bbox, text, confidence]] where bbox is (x1, y1, x2, y2).
    """
    if not results:
        return "No text detected."

    lines = [f"=== OCR Results ({len(results)} regions) ===", ""]
    for bbox, text, conf in results:
        x1, y1, x2, y2 = bbox
        lines.append(f"  [{x1},{y1},{x2},{y2}] \"{text}\" ({conf:.4f})")
    return "\n".join(lines)


def _format_detection_results(results: list, label: str) -> str:
    """
    Format detection results as text.

    Detection results are List[Tuple[bbox, label, confidence]].
    """
    if not results:
        return f"No {label.lower()} detected."

    lines = [f"=== {label} ({len(results)} found) ===", ""]
    for item in results:
        bbox, det_label, conf = item
        x1, y1, x2, y2 = bbox
        lines.append(f"  [{x1},{y1},{x2},{y2}] {det_label} ({conf:.4f})")
    return "\n".join(lines)
