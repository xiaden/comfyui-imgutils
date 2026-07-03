"""
Node: ImgUtilsPixAI — PixAI tagger.

Tags images using PixAI models with configurable threshold.
Returns general and character tags with IP association data.
"""

from __future__ import annotations

from comfy_api.latest import io

from ..utils import comfy_to_pil


class ImgUtilsPixAI(io.ComfyNode):
    """PixAI tagger — general and character tags with single threshold."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsPixAI",
            display_name="Imgutils PixAI Tagger",
            category="imgutils/tagging",
            description=(
                "Tag images using PixAI taggers. "
                "Returns general and character tags with IP data."
            ),
            search_aliases=[
                "pixai", "tagging", "ip", "caption", "describe",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to tag"),
                io.Float.Input(
                    "threshold", default=0.4, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold applied to all tag categories.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
                io.String.Output(display_name="scores"),
            ],
        )

    @classmethod
    def execute(cls, image, threshold) -> io.NodeOutput:
        from imgutils.tagging import get_pixai_tags

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = get_pixai_tags(
            pil_image,
            thresholds=float(threshold),
            fmt="tag",
        )

        sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)  # type: ignore[arg-type]
        tag_names = ", ".join(k for k, v in sorted_items[:50])
        tag_scores = "\n".join(f"  {k}: {v:.4f}" for k, v in sorted_items[:50])
        return io.NodeOutput(tag_names, tag_scores)
