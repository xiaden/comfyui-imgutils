"""Multi-label anime image classification — safety, NSFW, rating, style, character."""

import json
from comfy_api.latest import io
from .._shared.tensor import comfy_to_pil
from .._shared.formatting import label_display

class ImgUtilsClassify(io.ComfyNode):
    OPS = ["Safe Check", "NSFW Prediction", "Anime Rating", "Anime DB Rating", "Anime Teen",
           "Anime Classify", "Anime Real", "Anime Portrait", "Anime Furry",
           "Anime Bangumi Character", "Anime Style Age"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsClassify", display_name="Imgutils Classify",
            category="imgutils/judge",
            description="Classify anime images — safety, NSFW, content rating, style, and character detection.",
            search_aliases=["classify", "safety", "nsfw", "rating", "style", "character"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to classify."),
                io.Combo.Input("mode", options=cls.OPS, default="Safe Check", tooltip="What to classify — safety, NSFW, content rating, style, age, or character detection."),
            ],
            outputs=[io.String.Output(display_name="label"), io.Float.Output(display_name="score"), io.String.Output(display_name="json")],
        )

    @classmethod
    def execute(cls, image, mode) -> io.NodeOutput:
        from imgutils.validate import (
            safe_check_score, nsfw_pred_score, anime_rating_score, anime_dbrating_score,
            anime_teen_score, anime_classify_score, anime_real_score, anime_portrait_score,
            anime_furry_score, anime_bangumi_char_score, anime_style_age_score,
        )
        pil = comfy_to_pil(image)

        funcs = {
            "Safe Check": safe_check_score,
            "NSFW Prediction": nsfw_pred_score,
            "Anime Rating": anime_rating_score,
            "Anime DB Rating": anime_dbrating_score,
            "Anime Teen": anime_teen_score,
            "Anime Classify": anime_classify_score,
            "Anime Real": anime_real_score,
            "Anime Portrait": anime_portrait_score,
            "Anime Furry": anime_furry_score,
            "Anime Bangumi Character": anime_bangumi_char_score,
            "Anime Style Age": anime_style_age_score,
        }
        result = funcs[mode](pil)
        top = max(result, key=result.get)
        score = float(result[top])
        full = json.dumps({label_display(k): round(v, 4) for k, v in result.items()}, indent=2)
        return io.NodeOutput(label_display(top), score, full)
