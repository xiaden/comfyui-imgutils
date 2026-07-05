"""Case-insensitive substring membership check on label strings."""

from comfy_api.latest import io


class ImgUtilsLabelContains(io.ComfyNode):
    """Check whether a comma-separated label string contains a search term (case-insensitive)."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLabelContains",
            display_name="Imgutils Label Contains",
            category="imgutils/utility",
            description=(
                "Check whether a comma-separated label string contains a search term. "
                "Case-insensitive. Useful for branching on detection/tagging results."
            ),
            search_aliases=["contains", "label", "search", "filter", "match", "boolean"],
            inputs=[
                io.String.Input(
                    "labels",
                    tooltip="Comma-separated label string (e.g. from Detect or Tagging output).",
                ),
                io.String.Input(
                    "search",
                    tooltip="Term to search for in the labels. Case-insensitive.",
                ),
            ],
            outputs=[
                io.Boolean.Output(display_name="boolean"),
            ],
        )

    @classmethod
    def execute(cls, labels, search) -> io.NodeOutput:
        return io.NodeOutput(search.lower() in labels.lower())
