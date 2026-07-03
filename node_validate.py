"""
Node 1: ImgUtilsValidate — "What is this?"

Routes a dropdown to imgutils validate, metrics, and related functions.
Outputs: label (text only), score (float), full_response (JSON).

Dropdown options (18):
  Classification:
    safe_check, nsfw_pred, anime_rating, anime_dbrating, anime_teen,
    anime_classify, anime_real, anime_portrait, anime_furry,
    anime_bangumi_char, anime_style_age

  Boolean:
    is_ai_created, is_monochrome, is_greyscale, is_truncated, anime_completeness

  Numeric scores:
    get_monochrome_score, laplacian_score
"""

from __future__ import annotations

import json
import os
import tempfile

from comfy_api.latest import io

from .utils import comfy_to_pil


class ImgUtilsValidate(io.ComfyNode):
    """Validate/classify an image using imgutils functions."""

    DROPDOWN_OPTIONS = [
        "safe_check (~6 MB)",
        "nsfw_pred (~10 MB)",
        "anime_rating (~143 MB)",
        "anime_dbrating (~143 MB)",
        "anime_teen (~143 MB)",
        "anime_classify (~143 MB)",
        "anime_real (~143 MB)",
        "anime_portrait (~143 MB)",
        "anime_furry (~143 MB)",
        "anime_bangumi_char (~143 MB)",
        "anime_style_age (~143 MB)",
        "is_ai_created (~143 MB)",
        "is_monochrome (~143 MB)",
        "get_monochrome_score",
        "is_greyscale",
        "anime_completeness (~143 MB)",
        "is_truncated",
        "laplacian_score",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsValidate",
            display_name="Imgutils Judge",
            category="imgutils/validate",
            description=(
                "Validate and classify anime images — safety checks, NSFW detection, "
                "content ratings, style classification, monochrome/blur detection, "
                "and image completeness analysis."
            ),
            search_aliases=[
                "validate", "classify", "safety", "nsfw", "rating",
                "ai-detection", "monochrome", "blur", "sharpness",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to analyze"),
                io.Combo.Input(
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="safe_check",
                    tooltip="Select analysis operation.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="label"),
                io.Float.Output(display_name="score"),
                io.String.Output(display_name="full_response"),
            ],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        """
        Route the operation to the correct imgutils function.

        Returns:
            NodeOutput with (label: str, score: float, full_response: str)
            - label: top class name (classification), "true"/"false" (boolean),
                     or assessment text (numeric scores)
            - score: confidence score for classification, 1.0/0.0 for boolean,
                     raw value for numeric scores
            - full_response: JSON for classification, raw string for boolean,
                             detail string for numeric scores
        """
        operation = operation.split(" (")[0]  # strip size annotation

        from imgutils.metrics import laplacian_score
        from imgutils.validate import (
            anime_bangumi_char_score,
            anime_classify_score,
            anime_completeness,
            anime_dbrating_score,
            anime_furry_score,
            anime_portrait_score,
            anime_rating_score,
            anime_real_score,
            anime_style_age_score,
            anime_teen_score,
            get_monochrome_score,
            is_ai_created,
            is_greyscale,
            is_monochrome,
            is_truncated_file,
            nsfw_pred_score,
            safe_check_score,
        )

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        # ---- Classification functions (output dict: {class: score}) ----
        if operation == "safe_check":
            label, score, full = _format_classify(safe_check_score(pil_image))
        elif operation == "nsfw_pred":
            label, score, full = _format_classify(nsfw_pred_score(pil_image))
        elif operation == "anime_rating":
            label, score, full = _format_classify(anime_rating_score(pil_image))
        elif operation == "anime_dbrating":
            label, score, full = _format_classify(anime_dbrating_score(pil_image))
        elif operation == "anime_teen":
            label, score, full = _format_classify(anime_teen_score(pil_image))
        elif operation == "anime_classify":
            label, score, full = _format_classify(anime_classify_score(pil_image))
        elif operation == "anime_real":
            label, score, full = _format_classify(anime_real_score(pil_image))
        elif operation == "anime_portrait":
            label, score, full = _format_classify(anime_portrait_score(pil_image))
        elif operation == "anime_furry":
            label, score, full = _format_classify(anime_furry_score(pil_image))
        elif operation == "anime_bangumi_char":
            label, score, full = _format_classify(anime_bangumi_char_score(pil_image))
        elif operation == "anime_style_age":
            label, score, full = _format_classify(anime_style_age_score(pil_image))

        # ---- Boolean functions ----
        elif operation == "is_ai_created":
            result = is_ai_created(pil_image)
            label, score, full = ("true" if result else "false", 1.0 if result else 0.0, str(result))
        elif operation == "is_monochrome":
            result = is_monochrome(pil_image)
            label, score, full = ("true" if result else "false", 1.0 if result else 0.0, str(result))
        elif operation == "is_greyscale":
            result = is_greyscale(pil_image)
            label, score, full = ("true" if result else "false", 1.0 if result else 0.0, str(result))
        elif operation == "is_truncated":
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                pil_image.save(tmp, format="PNG")
                tmp_path = tmp.name
            try:
                result = is_truncated_file(tmp_path)
            finally:
                os.unlink(tmp_path)
            label, score, full = ("true" if result else "false", 1.0 if result else 0.0, str(result))
        elif operation == "anime_completeness":
            result = anime_completeness(pil_image)
            label, score, full = ("true" if result else "false", 1.0 if result else 0.0, str(result))

        # ---- Numeric scores ----
        elif operation == "get_monochrome_score":
            result = get_monochrome_score(pil_image)
            label, score, full = (f"{result:.4f}", float(result), f"Monochrome score: {result:.4f}")
        elif operation == "laplacian_score":
            result = laplacian_score(pil_image)
            threshold = 100
            quality = "sharp" if result >= threshold else "blurry"
            label, score, full = (quality, float(result),
                f"Laplacian score: {result:.2f}\nThreshold: {threshold} (lower = more blur)\nAssessment: {quality}")

        else:
            label, score, full = (f"Unknown operation: {operation}", 0.0, "")

        return io.NodeOutput(label, score, full)


def _format_classify(result: dict) -> tuple[str, float, str]:
    """
    Format a classification result dict as (label, score, full_response).

    label: top class name (text only, no score)
    score: top class score as float
    full_response: JSON of all class scores
    """
    if not result:
        return ("no results", 0.0, "{}")

    top_class = max(result, key=result.get)  # type: ignore[arg-type]
    top_score = float(result[top_class])

    full_str = json.dumps({k: round(v, 4) for k, v in result.items()}, indent=2)
    return (top_class, top_score, full_str)
