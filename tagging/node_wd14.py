"""WD14 (SmilingWolf) tagger — rating, general, and character tags."""

from comfy_api.latest import io

from ._base import _SectionedTagger


class ImgUtilsWD14(_SectionedTagger):
    """WD14 (SmilingWolf) tagger — rating, general, and character tags with per-category thresholds."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsWD14",
            display_name="Imgutils WD14 Tagger",
            category="imgutils/tagging",
            description=(
                "Tag images using WD14 (SmilingWolf) taggers. "
                "Returns rating, general tags, and character tags with confidence scores."
            ),
            search_aliases=[
                "wd14", "tagging", "swinv2", "convnext", "moat", "vit",
                "danbooru", "smilingwolf", "caption", "describe",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to tag."),
                io.Float.Input(
                    "general_threshold", default=0.35, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for general tags. Lower = more tags.",
                ),
                io.Float.Input(
                    "character_threshold", default=0.85, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for character tags. Higher = fewer false positives.",
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
    def execute(cls, image, general_threshold, character_threshold, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_wd14_tags

        return cls._run(image, get_wd14_tags,
                        general_threshold=general_threshold,
                        character_threshold=character_threshold,
                        drop_overlap=drop_overlap)

