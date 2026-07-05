"""MLDanbooru tagger — general tags only (no rating/character split)."""

import json

from comfy_api.latest import io

from .._shared.tensor import comfy_to_pil


class ImgUtilsMLDanbooru(io.ComfyNode):
    """MLDanbooru tagger — general tags only, single confidence threshold, top 50 returned."""

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
                io.Image.Input("image", tooltip="Input image to tag."),
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
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, threshold, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_mldanbooru_tags

        pil_image = comfy_to_pil(image)
        result = get_mldanbooru_tags(
            pil_image,
            threshold=threshold,
            drop_overlap=drop_overlap,
        )

        sorted_items = sorted(result.items(), key=lambda item: item[1], reverse=True)
        tag_names = ", ".join(k for k, v in sorted_items[:50])
        json_str = json.dumps(result, ensure_ascii=False)
        return io.NodeOutput(tag_names, json_str)
