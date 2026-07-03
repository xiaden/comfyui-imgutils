"""
Node: ImgUtilsCamie — Camie tagger.

Tags images using the Camie model with a threshold-preset mode.
Returns rating tags, general tags, and character tags.
"""

from __future__ import annotations

from comfy_api.latest import io

from ..utils import comfy_to_pil
from .node_wd14 import _join_names, _format_sections


class ImgUtilsCamie(io.ComfyNode):
    """Camie tagger — mode-based thresholds for 70,000+ tags."""

    MODES = ["balanced", "high_precision", "high_recall", "micro_opt", "macro_opt"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCamie",
            display_name="Imgutils Camie Tagger",
            category="imgutils/tagging",
            description=(
                "Tag images using the Camie tagger (70,000+ tags). "
                "Returns rating, general tags, and character tags."
            ),
            search_aliases=[
                "camie", "tagging", "70k", "caption", "describe",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to tag"),
                io.Combo.Input(
                    "mode", options=cls.MODES, default="balanced",
                    tooltip="Threshold preset: balanced, high_precision, high_recall, micro_opt, or macro_opt.",
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
    def execute(cls, image, mode, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_camie_tags

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        rating, general, character = get_camie_tags(
            pil_image,
            mode=str(mode),
            drop_overlap=bool(drop_overlap),
        )

        tag_names = _join_names(rating, general, character)
        tag_scores = _format_sections(
            ("Rating", rating), ("General Tags", general), ("Characters", character),
        )
        return io.NodeOutput(tag_names, tag_scores)
