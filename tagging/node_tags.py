"""Tag string processing — filter, sort, and format Danbooru-style tags."""

from collections.abc import Mapping

from comfy_api.latest import io


class ImgUtilsTags(io.ComfyNode):
    """Filter, sort, deduplicate, and format Danbooru tag strings."""

    DROPDOWN_OPTIONS = [
        "Drop Blacklisted",
        "Drop Basic Character",
        "Drop Overlap",
        "Sort Original",
        "Sort by Score",
        "Shuffle",
        "Spaces to Underscores",
        "Underscores to Spaces",
        "Format Text",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsTags",
            display_name="Imgutils Tags",
            category="imgutils/tagging",
            description=(
                "Process tag strings — filter blacklisted/basic-character/overlapping tags, "
                "sort by original order or score, convert between underscore/space formats, "
                "and format as training-ready text."
            ),
            search_aliases=[
                "tags", "tagging", "filter", "blacklist",
                "sort", "format", "underscore", "danbooru",
                "wd14", "clean", "deduplicate",
            ],
            inputs=[
                io.String.Input(
                    "tags",
                    multiline=True,
                    tooltip="Tags to process. Comma-separated or newline-separated. "
                    "Optionally include scores as 'tag: 0.95'.",
                ),
                io.Combo.Input(
                    "mode",
                    options=cls.DROPDOWN_OPTIONS,
                    default="Drop Blacklisted",
                    tooltip="Processing operation — filtering, sorting, format conversion, or text formatting.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
            ],
        )

    @classmethod
    def execute(cls, tags, mode) -> io.NodeOutput:
        from imgutils.tagging import (
            drop_blacklisted_tags, drop_basic_character_tags, drop_overlap_tags,
            sort_tags, add_underline, remove_underline, tags_to_text,
        )

        parsed = _parse_tags(tags)

        _FILTERS = {
            "Drop Blacklisted": drop_blacklisted_tags,
            "Drop Basic Character": drop_basic_character_tags,
            "Drop Overlap": drop_overlap_tags,
        }
        if mode in _FILTERS:
            return io.NodeOutput(_format_tags(_FILTERS[mode](parsed)))

        _SORT_MODES = {"Sort Original": "original", "Sort by Score": "score", "Shuffle": "shuffle"}
        if mode in _SORT_MODES:
            return io.NodeOutput(_format_tags(sort_tags(parsed, mode=_SORT_MODES[mode])))

        if mode in ("Spaces to Underscores", "Underscores to Spaces"):
            transform = add_underline if mode == "Spaces to Underscores" else remove_underline
            if isinstance(parsed, dict):
                result = {transform(k): v for k, v in parsed.items()}
            else:
                result = [transform(t) for t in parsed]
            return io.NodeOutput(_format_tags(result))

        if mode == "Format Text":
            if not isinstance(parsed, dict):
                parsed = {t: 1.0 for t in parsed}
            return io.NodeOutput(tags_to_text(parsed, use_spaces=False, use_escape=True, include_score=False))

        return io.NodeOutput(tags)


def _parse_tags(text: str) -> list[str] | dict[str, float]:
    """Parse a tag string into a list of tags or a dict of {tag: score}."""

    raw_tokens = [t.strip() for t in text.replace("\n", ",").split(",")]
    tokens = [t for t in raw_tokens if t]

    if not tokens:
        return []

    has_scores = False
    parsed: dict[str, float] = {}
    for token in tokens:
        if ":" in token:
            tag, _, score_str = token.rpartition(":")
            try:
                score = float(score_str.strip())
                parsed[tag.strip()] = score
                has_scores = True
                continue
            except ValueError:
                pass
        parsed[token.strip()] = 1.0

    if has_scores:
        return parsed
    return tokens


def _format_tags(tags: list[str] | Mapping[str, float]) -> str:
    """Format parsed tags back to a string."""
    if isinstance(tags, Mapping):
        return ", ".join(f"{k}: {v:.4f}" for k, v in tags.items())
    else:
        return ", ".join(tags)
