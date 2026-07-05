"""Merge and deduplicate multiple tag strings into a single case-insensitive sorted list."""

from comfy_api.latest import io


class ImgUtilsDedup(io.ComfyNode):
    """Merge multiple tag strings, deduplicate case-insensitively, output unique list."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsDedup",
            display_name="Imgutils Deduplicate Tags",
            category="imgutils/utility",
            description=(
                "Merge multiple tag strings into one comma-separated list, "
                "removing duplicates. Connect multiple tag sources to the single input."
            ),
            search_aliases=["deduplicate", "dedup", "merge", "tags", "unique", "combine"],
            is_input_list=True,
            inputs=[
                io.String.Input(
                    "tags",
                    tooltip="Tag strings to merge. Connect multiple inputs — they will be combined and deduplicated.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="tags"),
                io.Int.Output(display_name="count"),
            ],
        )

    @classmethod
    def execute(cls, tags) -> io.NodeOutput:
        all_tags: list[str] = []
        for tag_str in tags:
            for t in tag_str.replace("\n", ",").split(","):
                stripped = t.strip()
                if stripped:
                    all_tags.append(stripped)

        seen: set[str] = set()
        unique: list[str] = []
        for t in all_tags:
            if t.lower() not in seen:
                seen.add(t.lower())
                unique.append(t)

        return io.NodeOutput(", ".join(unique), len(unique))
