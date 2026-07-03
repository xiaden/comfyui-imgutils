"""Node: ImgUtilsClassify — Multi-label anime image classification."""
from __future__ import annotations
import json, os, tempfile
from comfy_api.latest import io
from ..utils import comfy_to_pil

class ImgUtilsClassify(io.ComfyNode):
    OPS = ["safe_check", "nsfw_pred", "anime_rating", "anime_dbrating", "anime_teen",
           "anime_classify", "anime_real", "anime_portrait", "anime_furry",
           "anime_bangumi_char", "anime_style_age"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsClassify", display_name="Imgutils Classify",
            category="imgutils/judge",
            description="Classify anime images — safety, NSFW, content rating, style, and character detection.",
            search_aliases=["classify", "safety", "nsfw", "rating", "style", "character"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Combo.Input("operation", options=cls.OPS, default="safe_check", tooltip="Classification type."),
            ],
            outputs=[io.String.Output(display_name="label"), io.Float.Output(display_name="score"), io.String.Output(display_name="full_response")],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        from imgutils.validate import (
            safe_check_score, nsfw_pred_score, anime_rating_score, anime_dbrating_score,
            anime_teen_score, anime_classify_score, anime_real_score, anime_portrait_score,
            anime_furry_score, anime_bangumi_char_score, anime_style_age_score,
        )
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        funcs = {
            "safe_check": safe_check_score, "nsfw_pred": nsfw_pred_score,
            "anime_rating": anime_rating_score, "anime_dbrating": anime_dbrating_score,
            "anime_teen": anime_teen_score, "anime_classify": anime_classify_score,
            "anime_real": anime_real_score, "anime_portrait": anime_portrait_score,
            "anime_furry": anime_furry_score, "anime_bangumi_char": anime_bangumi_char_score,
            "anime_style_age": anime_style_age_score,
        }
        result = funcs.get(operation, lambda p: {})(pil)
        if not result:
            return io.NodeOutput("no results", 0.0, "{}")
        top = max(result, key=result.get)  # type: ignore[arg-type]
        score = float(result[top])
        full = json.dumps({k: round(v, 4) for k, v in result.items()}, indent=2)
        return io.NodeOutput(top, score, full)
