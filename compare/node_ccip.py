"""CCIP character identity similarity — lower distance = more similar."""

from comfy_api.latest import io
from .._shared.tensor import comfy_to_pil
from ._distance import _distance_label

CCIP_THRESHOLDS: list[tuple[float, str]] = [
    (0.10, "exact"),
    (0.25, "very similar"),
    (0.40, "similar"),
    (0.60, "different"),
    (0.80, "very different"),
    (float("inf"), "opposite"),
]


class ImgUtilsCCIP(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCCIP", display_name="Imgutils Compare (CCIP)",
            category="imgutils/compare",
            description="Compare anime character identity using CCIP distance. Lower = more similar.",
            search_aliases=["compare", "ccip", "character", "similarity", "distance"],
            inputs=[
                io.Image.Input("image_a", tooltip="First image to compare."),
                io.Image.Input("image_b", tooltip="Second image for comparison."),
            ],
            outputs=[
                io.String.Output(display_name="label"),
                io.Float.Output(display_name="distance"),
            ],
        )

    @classmethod
    def execute(cls, image_a, image_b) -> io.NodeOutput:
        from imgutils.metrics import ccip_difference

        pil_a = comfy_to_pil(image_a)
        pil_b = comfy_to_pil(image_b)
        distance = ccip_difference(pil_a, pil_b)
        label = _distance_label(distance, CCIP_THRESHOLDS)
        return io.NodeOutput(label, distance)
