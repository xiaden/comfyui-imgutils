"""
Node 2: ImgUtilsDescribe — "Describe this"

Routes a dropdown to imgutils tagging and OCR functions.
Outputs clean tag names and tag-name-with-scores as separate outputs.

Dropdown options (8):
  Tagging:
    get_wd14_tags         -> imgutils.tagging.get_wd14_tags()
    get_deepdanbooru_tags -> imgutils.tagging.get_deepdanbooru_tags()
    get_mldanbooru_tags   -> imgutils.tagging.get_mldanbooru_tags()
    camie_tags            -> imgutils.tagging.get_camie_tags()
    deepgelbooru_tags     -> imgutils.tagging.get_deepgelbooru_tags()
    pixai_tags            -> imgutils.tagging.get_pixai_tags()

  OCR:
    ocr                   -> imgutils.ocr.ocr()
    detect_text_with_ocr  -> imgutils.ocr.detect_text_with_ocr()
"""

from __future__ import annotations

from comfy_api.latest import io

from .utils import comfy_to_pil


class ImgUtilsDescribe(io.ComfyNode):
    """Describe an image using imgutils tagging and OCR."""

    DROPDOWN_OPTIONS = [
        "get_wd14_tags",
        "get_deepdanbooru_tags",
        "get_mldanbooru_tags",
        "camie_tags",
        "deepgelbooru_tags",
        "pixai_tags",
        "ocr",
        "detect_text_with_ocr",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsDescribe",
            display_name="Imgutils Describe",
            category="imgutils/describe",
            description=(
                "Tag and describe anime images — WD14, DeepDanbooru, MLDanbooru, "
                "Camie, and PixAI tagging, plus OCR text extraction."
            ),
            search_aliases=[
                "describe", "tagging", "wd14", "deepdanbooru", "mldanbooru",
                "camie", "pixai", "ocr", "tags", "caption",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to analyze"),
                io.Combo.Input(
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="get_wd14_tags",
                    tooltip="Select operation: WD14/DeepDanbooru/MLDanbooru/Camie/PixAI tagging, or OCR.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
                io.String.Output(display_name="scores"),
            ],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        """
        Route the operation to the correct imgutils function.

        Returns:
            NodeOutput with (tags: str, scores: str)
            - tags: comma-separated tag names only (no scores)
            - scores: tags with confidence scores, formatted as text
        """
        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        # ---- Tagging functions ----
        if operation == "get_wd14_tags":
            from imgutils.tagging import get_wd14_tags

            rating, general, character = get_wd14_tags(pil_image)
            return io.NodeOutput(
                _format_tag_names_wd14(rating, general, character),
                _format_tag_scores_wd14(rating, general, character),
            )

        elif operation in ("get_deepdanbooru_tags", "get_mldanbooru_tags",
                           "camie_tags", "deepgelbooru_tags", "pixai_tags"):
            tags, scores = _run_tagger(pil_image, operation)
            return io.NodeOutput(tags, scores)

        # ---- OCR functions ----
        elif operation == "ocr":
            from imgutils.ocr import ocr

            results = ocr(pil_image)
            tags, scores = _format_ocr(results, include_confidence=True)
            return io.NodeOutput(tags, scores)

        elif operation == "detect_text_with_ocr":
            from imgutils.ocr import detect_text_with_ocr

            results = detect_text_with_ocr(pil_image)
            tags, scores = _format_ocr(results, include_confidence=False)
            return io.NodeOutput(tags, scores)

        else:
            return io.NodeOutput(f"Unknown operation: {operation}", "")


def _run_tagger(pil_image, operation: str) -> tuple[str, str]:
    """Run a tagger and return (tag_names_only, tags_with_scores)."""
    tagger_map = {
        "get_deepdanbooru_tags": "imgutils.tagging.get_deepdanbooru_tags",
        "get_mldanbooru_tags": "imgutils.tagging.get_mldanbooru_tags",
        "camie_tags": "imgutils.tagging.get_camie_tags",
        "deepgelbooru_tags": "imgutils.tagging.get_deepgelbooru_tags",
        "pixai_tags": "imgutils.tagging.get_pixai_tags",
    }

    module_name, func_name = tagger_map[operation].rsplit(".", 1)
    import importlib

    mod = importlib.import_module(module_name)
    tag_dict = getattr(mod, func_name)(pil_image)

    if not isinstance(tag_dict, dict):
        return (str(tag_dict), str(tag_dict))

    sorted_items = sorted(tag_dict.items(), key=lambda x: x[1], reverse=True)  # type: ignore[arg-type]
    tag_names = ", ".join(k for k, v in sorted_items[:50])
    tag_scores = "\n".join(f"  {k}: {v:.4f}" for k, v in sorted_items[:50])

    return (tag_names, tag_scores)


def _format_tag_names_wd14(rating: dict, general: dict, character: dict) -> str:
    """WD14 tag names only — comma-separated, no scores."""
    parts = []
    for d in (rating, general, character):
        sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)  # type: ignore[arg-type]
        parts.extend(k for k, v in sorted_items)
    return ", ".join(parts)


def _format_tag_scores_wd14(rating: dict, general: dict, character: dict) -> str:
    """WD14 tags with scores — structured text."""
    lines = ["=== WD14 Tags ===", ""]
    for section, d in [("Rating", rating), ("General Tags", general), ("Characters", character)]:
        lines.append(f"## {section}")
        for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):  # type: ignore[arg-type]
            lines.append(f"  {k}: {v:.4f}")
        lines.append("")
    return "\n".join(lines)


def _format_ocr(results: list, include_confidence: bool) -> tuple[str, str]:
    """
    Format OCR results as (tag_names, tag_scores).

    OCR results are List[Tuple[bbox, text, confidence]].
    """
    if not results:
        return ("No text detected.", "No text detected.")

    if include_confidence:
        tags = ", ".join(f'"{text}"' for bbox, text, conf in results)
        scores = "\n".join(
            f"  [{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}] \"{text}\" ({conf:.4f})"
            for bbox, text, conf in results
        )
        return (tags, scores)
    else:
        tags = ", ".join(f"[{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}]" for bbox, text, conf in results)
        return (tags, tags)
