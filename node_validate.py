"""
Node 1: ImgUtilsValidate — "What is this?"

Routes a dropdown to imgutils validate, metrics, and related functions.
Outputs a short call result and a detailed full_response.

Dropdown options (19):
  Classification (output dict of class scores -> top in call, full JSON in full_response):
    safe_check         -> imgutils.validate.safe.safe_check_score()
    nsfw_pred          -> imgutils.validate.nsfw.nsfw_pred_score()
    anime_rating       -> imgutils.validate.rating.anime_rating_score()
    anime_dbrating     -> imgutils.validate.dbrating.anime_dbrating_score()
    anime_teen         -> imgutils.validate.teen.anime_teen_score()
    anime_classify     -> imgutils.validate.classify.anime_classify_score()
    anime_real         -> imgutils.validate.real.anime_real_score()
    anime_portrait     -> imgutils.validate.portrait.anime_portrait_score()
    anime_furry        -> imgutils.validate.furry.anime_furry_score()
    anime_bangumi_char -> imgutils.validate.bangumi_char.anime_bangumi_char_score()
    anime_style_age    -> imgutils.validate.style_age.anime_style_age_score()

  Boolean (true/false in call):
    is_ai_created      -> imgutils.validate.aicheck.is_ai_created()
    is_monochrome      -> imgutils.validate.monochrome.is_monochrome()
    is_greyscale       -> imgutils.validate.color.is_greyscale()
    is_truncated       -> imgutils.validate.truncate.is_truncated_file() [needs file path]
    anime_completeness -> imgutils.validate.completeness.anime_completeness()

  Numeric scores:
    get_monochrome_score -> imgutils.validate.monochrome.get_monochrome_score()
    laplacian_score    -> imgutils.metrics.laplacian.laplacian_score()

  Aesthetic scoring:
    anime_dbaesthetic    -> imgutils.metrics.anime_dbaesthetic()
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
        "safe_check",
        "nsfw_pred",
        "anime_rating",
        "anime_dbrating",
        "anime_teen",
        "anime_classify",
        "anime_real",
        "anime_portrait",
        "anime_furry",
        "anime_bangumi_char",
        "anime_style_age",
        "is_ai_created",
        "is_monochrome",
        "get_monochrome_score",
        "is_greyscale",
        "anime_completeness",
        "is_truncated",
        "laplacian_score",
        "anime_dbaesthetic",
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
                "image completeness analysis, and Danbooru aesthetic scoring."
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
                    tooltip="Select analysis operation: safety check, NSFW prediction, content rating, style classification, sharpness, aesthetic scoring, etc.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="call"),
                io.String.Output(display_name="full_response"),
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
            NodeOutput with (call_string, full_response_string)
        """
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

        # ---- Classification functions (output dict) ----
        if operation == "safe_check":
            result = safe_check_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Safety check"))

        elif operation == "nsfw_pred":
            result = nsfw_pred_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "NSFW prediction"))

        elif operation == "anime_rating":
            result = anime_rating_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Anime rating"))

        elif operation == "anime_dbrating":
            result = anime_dbrating_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Danbooru rating"))

        elif operation == "anime_teen":
            result = anime_teen_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Teen detection"))

        elif operation == "anime_classify":
            result = anime_classify_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Anime classification"))

        elif operation == "anime_real":
            result = anime_real_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Anime vs real"))

        elif operation == "anime_portrait":
            result = anime_portrait_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Portrait detection"))

        elif operation == "anime_furry":
            result = anime_furry_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Furry detection"))

        elif operation == "anime_bangumi_char":
            result = anime_bangumi_char_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Bangumi character"))

        elif operation == "anime_style_age":
            result = anime_style_age_score(pil_image)
            return io.NodeOutput(*_format_classify(result, "Style age"))

        # ---- Boolean functions ----
        elif operation == "is_ai_created":
            result = is_ai_created(pil_image)
            return io.NodeOutput("true" if result else "false", str(result))

        elif operation == "is_monochrome":
            result = is_monochrome(pil_image)
            return io.NodeOutput("true" if result else "false", str(result))

        elif operation == "is_greyscale":
            result = is_greyscale(pil_image)
            return io.NodeOutput("true" if result else "false", str(result))

        elif operation == "is_truncated":
            # is_truncated_file requires a file path, not a PIL Image
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                pil_image.save(tmp, format="PNG")
                tmp_path = tmp.name
            try:
                result = is_truncated_file(tmp_path)
            finally:
                os.unlink(tmp_path)
            return io.NodeOutput("true" if result else "false", str(result))

        elif operation == "anime_completeness":
            result = anime_completeness(pil_image)
            return io.NodeOutput("true" if result else "false", str(result))

        # ---- Numeric scores ----
        elif operation == "get_monochrome_score":
            result = get_monochrome_score(pil_image)
            return io.NodeOutput(f"{result:.4f}", f"Monochrome score: {result:.4f}")

        elif operation == "laplacian_score":
            result = laplacian_score(pil_image)
            threshold = 100
            quality = "sharp" if result >= threshold else "blurry"
            call_str = f"{result:.2f} ({quality})"
            full_str = (
                f"Laplacian score: {result:.2f}\n"
                f"Threshold: {threshold} (lower = more blur)\n"
                f"Assessment: {quality}"
            )
            return io.NodeOutput(call_str, full_str)

        # ---- Aesthetic scoring ----
        elif operation == "anime_dbaesthetic":
            from imgutils.metrics import anime_dbaesthetic

            overall, scores = anime_dbaesthetic(pil_image)
            call_str = f"aesthetic: {overall:.4f}"
            full_lines = [f"Danbooru Aesthetic Score: {overall:.4f}", ""]
            for label in ("masterpiece", "best", "great", "good", "normal", "low", "worst"):
                if label in scores:
                    full_lines.append(f"  {label}: {scores[label]:.4f}")
            return io.NodeOutput(call_str, "\n".join(full_lines))

        else:
            return io.NodeOutput(f"Unknown operation: {operation}", "")


def _format_classify(result: dict, label: str) -> tuple[str, str]:
    """
    Format a classification result dict as (call, full_response).

    call: top class name + score
    full_response: JSON of all class scores
    """
    if not result:
        return (f"{label}: no results", "{}")

    # Find top class
    top_class = max(result, key=result.get)  # type: ignore[arg-type]  # result is dict[str, float], mypy infers too narrow for key func
    top_score = result[top_class]

    call_str = f"{top_class}: {top_score:.4f}"
    full_str = json.dumps({k: round(v, 4) for k, v in result.items()}, indent=2)
    return (call_str, full_str)
