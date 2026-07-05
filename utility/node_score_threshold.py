"""Score versus threshold boolean gate for workflow branching."""

from comfy_api.latest import io


class ImgUtilsScoreThreshold(io.ComfyNode):
    """Compare a float score against a threshold, output True if score >= threshold."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsScoreThreshold",
            display_name="Imgutils Score Threshold",
            category="imgutils/utility",
            description=(
                "Compare a score against a threshold value. "
                "Outputs True if score >= threshold. Useful for gating workflows."
            ),
            search_aliases=["threshold", "score", "boolean", "gate", "compare", "filter"],
            inputs=[
                io.Float.Input("score", default=0.5, min=0.0, max=1.0, step=0.01, tooltip="Score value to evaluate."),
                io.Float.Input("threshold", default=0.5, min=0.0, max=1.0, step=0.01, tooltip="Threshold to compare against."),
            ],
            outputs=[
                io.Boolean.Output(display_name="boolean"),
            ],
        )

    @classmethod
    def execute(cls, score, threshold) -> io.NodeOutput:
        return io.NodeOutput(score >= threshold)
