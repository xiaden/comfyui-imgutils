"""PixAI tagger — general and character tags with IP association data."""

import json

from comfy_api.latest import io

from .._shared.tensor import comfy_to_pil


class ImgUtilsPixAI(io.ComfyNode):
    """PixAI tagger — general and character tags with IP metadata, single threshold."""

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
                io.Image.Input("image", tooltip="Input image to tag."),
                io.Float.Input(
                    "threshold", default=0.4, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold applied to all tag categories.",
                ),
                io.Boolean.Input(
                    "drop_overlap", default=False,
                    tooltip="Remove overlapping/redundant tags.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, threshold, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_pixai_tags, drop_overlap_tags as _drop_overlap_tags

        pil_image = comfy_to_pil(image)
        result = get_pixai_tags(
            pil_image,
            thresholds=threshold,
            fmt="tag",
        )

        if drop_overlap:
            result = _drop_overlap_tags(result)

        sorted_items = sorted(result.items(), key=lambda item: item[1], reverse=True)
        tag_names = ", ".join(k for k, v in sorted_items[:50])
        json_str = json.dumps(result, ensure_ascii=False)
        return io.NodeOutput(tag_names, json_str)
