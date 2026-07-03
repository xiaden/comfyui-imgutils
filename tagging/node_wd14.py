"""
Node: ImgUtilsWD14 — WD14 tagger with full threshold control.

Tags images using the SmilingWolf WD14 family of models.
Returns rating tags, general tags, and character tags.
"""

from __future__ import annotations

from comfy_api.latest import io

from ..utils import comfy_to_pil


class ImgUtilsWD14(io.ComfyNode):
    """WD14 tagger — general and character tags with confidence thresholds."""

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
                io.Image.Input("image", tooltip="Input image to tag"),
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
                io.String.Output(display_name="scores"),
            ],
        )

    @classmethod
    def execute(cls, image, general_threshold, character_threshold, drop_overlap=False) -> io.NodeOutput:
        from imgutils.tagging import get_wd14_tags

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        rating, general, character = get_wd14_tags(
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


def _join_names(*sections: dict) -> str:
    """Join tag names from multiple dict sections into comma-separated list."""
    parts = []
    for d in sections:
        parts.extend(k for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True))  # type: ignore[arg-type]
    return ", ".join(parts)


def _format_sections(*sections: tuple[str, dict]) -> str:
    """Format tag dicts with scores as structured text."""
    lines = []
    for title, d in sections:
        if not d:
            continue
        lines.append(f"## {title}")
        for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):  # type: ignore[arg-type]
            lines.append(f"  {k}: {v:.4f}")
        lines.append("")
    return "\n".join(lines)
