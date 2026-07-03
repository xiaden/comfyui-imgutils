"""
Node: ImgUtilsDeepDanbooru — DeepDanbooru tagger.

Tags images using the DeepDanbooru model with configurable thresholds.
"""

from __future__ import annotations

from comfy_api.latest import io

from ..utils import comfy_to_pil
from .node_wd14 import _join_names, _format_sections


class ImgUtilsDeepDanbooru(io.ComfyNode):
    """DeepDanbooru tagger — general and character tags with confidence thresholds."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsDeepDanbooru",
            display_name="Imgutils DeepDanbooru Tagger",
            category="imgutils/tagging",
            description=(
                "Tag images using the DeepDanbooru model. "
                "Returns rating, general tags, and character tags with confidence scores."
            ),
            search_aliases=[
                "deepdanbooru", "tagging", "danbooru", "caption", "describe",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to tag"),
                io.Float.Input(
                    "general_threshold", default=0.5, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for general tags.",
                ),
                io.Float.Input(
                    "character_threshold", default=0.5, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for character tags.",
                ),
                io.Boolean.Input(
                    "drop_overlap", default=False,
                    tooltip="Remove overlapping/redundant tags.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
                io.String.Output(display_name="scores"),
            ],
        )

    @classmethod
    def execute(cls, image, general_threshold, character_threshold, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_deepdanbooru_tags

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        rating, general, character = get_deepdanbooru_tags(
            pil_image,
            general_threshold=float(general_threshold),
            character_threshold=float(character_threshold),
            drop_overlap=bool(drop_overlap),
        )

        tag_names = _join_names(rating, general, character)
        tag_scores = _format_sections(
            ("Rating", rating), ("General Tags", general), ("Characters", character),
        )
        return io.NodeOutput(tag_names, tag_scores)
