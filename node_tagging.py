"""
Node 7: ImgUtilsTags — "Process tag strings"

Text-in/text-out tag processing using imgutils.tagging utilities.
Parses comma-separated or newline-separated tag strings (with optional scores),
applies filtering/sorting/formatting operations, and outputs processed tags.

Dropdown options (9):
  drop_blacklisted       -> imgutils.tagging.drop_blacklisted_tags()
  drop_basic_character   -> imgutils.tagging.drop_basic_character_tags()
  drop_overlap           -> imgutils.tagging.drop_overlap_tags()
  sort_original          -> imgutils.tagging.sort_tags(mode='original')
  sort_score             -> imgutils.tagging.sort_tags(mode='score')
  sort_shuffle           -> imgutils.tagging.sort_tags(mode='shuffle')
  spaces_to_underscores  -> imgutils.tagging.add_underline()
  underscores_to_spaces  -> imgutils.tagging.remove_underline()
  format_text            -> imgutils.tagging.tags_to_text()
"""

from __future__ import annotations

from comfy_api.latest import io


class ImgUtilsTags(io.ComfyNode):
    """Process and transform tag strings using imgutils.tagging utilities."""

    DROPDOWN_OPTIONS = [
        "drop_blacklisted",
        "drop_basic_character",
        "drop_overlap",
        "sort_original",
        "sort_score",
        "sort_shuffle",
        "spaces_to_underscores",
        "underscores_to_spaces",
        "format_text",
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
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="drop_blacklisted",
                    tooltip="Processing operation — filtering, sorting, format conversion, or text formatting.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
            ],
        )

    @classmethod
    def execute(cls, tags, operation) -> io.NodeOutput:
        """
        Parse tag string, apply the selected operation, and return processed output.

        Args:
            tags: input tag string (comma or newline separated, optional scores)
            operation: dropdown selection

        Returns:
            NodeOutput with processed tag string
        """
        parsed, is_dict = _parse_tags(tags)

        if operation == "drop_blacklisted":
            from imgutils.tagging import drop_blacklisted_tags

            result = drop_blacklisted_tags(parsed)
            return io.NodeOutput(_format_tags(result))

        elif operation == "drop_basic_character":
            from imgutils.tagging import drop_basic_character_tags

            result = drop_basic_character_tags(parsed)
            return io.NodeOutput(_format_tags(result))

        elif operation == "drop_overlap":
            from imgutils.tagging import drop_overlap_tags

            result = drop_overlap_tags(parsed)
            return io.NodeOutput(_format_tags(result))

        elif operation == "sort_original":
            from imgutils.tagging import sort_tags

            result = sort_tags(parsed, mode="original")
            return io.NodeOutput(_format_tags(result))

        elif operation == "sort_score":
            from imgutils.tagging import sort_tags

            result = sort_tags(parsed, mode="score")
            return io.NodeOutput(_format_tags(result))

        elif operation == "sort_shuffle":
            from imgutils.tagging import sort_tags

            result = sort_tags(parsed, mode="shuffle")
            return io.NodeOutput(_format_tags(result))

        elif operation == "spaces_to_underscores":
            from imgutils.tagging import add_underline

            if is_dict:
                result = {add_underline(k): v for k, v in parsed.items()}
            else:
                result = [add_underline(t) for t in parsed]
            return io.NodeOutput(_format_tags(result))

        elif operation == "underscores_to_spaces":
            from imgutils.tagging import remove_underline

            if is_dict:
                result = {remove_underline(k): v for k, v in parsed.items()}
            else:
                result = [remove_underline(t) for t in parsed]
            return io.NodeOutput(_format_tags(result))

        elif operation == "format_text":
            from imgutils.tagging import tags_to_text

            if not is_dict:
                # Convert list to dict with uniform scores for formatting
                parsed = {t: 1.0 for t in parsed}
            result = tags_to_text(parsed, use_spaces=False, use_escape=True, include_score=False)
            return io.NodeOutput(result)

        else:
            return io.NodeOutput(tags)


def _parse_tags(text: str) -> tuple[list[str] | dict[str, float], bool]:
    """
    Parse a tag string into either a list of strings or a dict of {tag: score}.

    Detection logic:
    - Split by comma or newline
    - If tokens contain ':' followed by a parseable float → dict mode
    - Otherwise → list mode
    """
    # Split by comma or newline, strip whitespace, filter empty
    raw_tokens = [t.strip() for t in text.replace("\n", ",").split(",")]
    tokens = [t for t in raw_tokens if t]

    if not tokens:
        return [], False

    # Check if tokens look like scored tags ("tag: 0.95")
    scored = False
    for token in tokens:
        if ":" in token:
            parts = token.rsplit(":", 1)
            try:
                float(parts[1].strip())
                scored = True
                break
            except ValueError:
                pass

    if scored:
        result = {}
        for token in tokens:
            if ":" in token:
                parts = token.rsplit(":", 1)
                try:
                    score = float(parts[1].strip())
                    tag = parts[0].strip()
                    result[tag] = score
                except ValueError:
                    result[token.strip()] = 1.0
            else:
                result[token.strip()] = 1.0
        return result, True
    else:
        return tokens, False


def _format_tags(tags) -> str:
    """Format parsed tags back to a string."""
    if isinstance(tags, dict):
        return ", ".join(f"{k}: {v:.4f}" for k, v in tags.items())
    else:
        return ", ".join(tags)
