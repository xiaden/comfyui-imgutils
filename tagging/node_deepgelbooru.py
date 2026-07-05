"""DeepGelbooru tagger — rating, general, and character tags."""

from comfy_api.latest import io

from ._base import _SectionedTagger


class ImgUtilsDeepGelbooru(_SectionedTagger):
    """DeepGelbooru tagger — rating, general, and character tags with configurable thresholds."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsDeepGelbooru",
            display_name="Imgutils DeepGelbooru Tagger",
            category="imgutils/tagging",
            description=(
                "Tag images using the DeepGelbooru model. "
                "Returns rating, general tags, and character tags with confidence scores."
            ),
            search_aliases=[
                "deepgelbooru", "tagging", "gelbooru", "caption", "describe",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to tag."),
                io.Float.Input(
                    "general_threshold", default=0.3, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for general tags.",
                ),
                io.Float.Input(
                    "character_threshold", default=0.3, min=0.0, max=1.0, step=0.05,
                    tooltip="Confidence threshold for character tags.",
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
        from imgutils.tagging import get_deepgelbooru_tags

        return cls._run(image, get_deepgelbooru_tags,
                        general_threshold=general_threshold,
                        character_threshold=character_threshold,
                        drop_overlap=drop_overlap)
