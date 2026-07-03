"""
Node: ImgUtilsMLDanbooru — MLDanbooru tagger.

Tags images using the ML-Danbooru model with a single confidence threshold.
Returns general tags only (no rating/character split).
"""

from __future__ import annotations

from comfy_api.latest import io

from ..utils import comfy_to_pil


class ImgUtilsMLDanbooru(io.ComfyNode):
    """MLDanbooru tagger — general tags with a single confidence threshold."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsMLDanbooru",
            display_name="Imgutils MLDanbooru Tagger",
            category="imgutils/tagging",
            description=(
                "Tag images using the ML-Danbooru model. "
                "Returns general tags with confidence scores (no rating/character split)."
            ),
            search_aliases=[
                "mldanbooru", "tagging", "danbooru", "caption", "describe",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to tag"),
                io.Float.Input(
                    "threshold", default=0.7, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for all tags.",
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
    def execute(cls, image, threshold, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_mldanbooru_tags

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = get_mldanbooru_tags(
            pil_image,
            threshold=float(threshold),
            drop_overlap=bool(drop_overlap),
        )

        sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)  # type: ignore[arg-type]
        tag_names = ", ".join(k for k, v in sorted_items[:50])
        tag_scores = "\n".join(f"  {k}: {v:.4f}" for k, v in sorted_items[:50])
        return io.NodeOutput(tag_names, tag_scores)
