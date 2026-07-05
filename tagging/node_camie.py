"""Camie tagger (70,000+ tags) — rating, general, and character tags with threshold-preset mode."""

from comfy_api.latest import io

from ._base import _SectionedTagger


class ImgUtilsCamie(_SectionedTagger):
    """Camie tagger — 70,000+ tags, mode-based threshold presets."""

    MODES = ["Balanced", "High Precision", "High Recall", "Micro Optimized", "Macro Optimized"]

    _MODE_API = {
        "Balanced": "balanced",
        "High Precision": "high_precision",
        "High Recall": "high_recall",
        "Micro Optimized": "micro_opt",
        "Macro Optimized": "macro_opt",
    }

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
                io.Image.Input("image", tooltip="Input image to tag."),
                io.Combo.Input(
                    "mode", options=cls.MODES, default="Balanced",
                    tooltip="Threshold preset for tag selection.",
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
    def execute(cls, image, mode, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_camie_tags

        return cls._run(image, get_camie_tags,
                        mode=cls._MODE_API.get(mode, mode),
                        drop_overlap=drop_overlap)
