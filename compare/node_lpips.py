"""LPIPS perceptual similarity — lower distance = more similar."""

from comfy_api.latest import io
from .._shared.tensor import comfy_to_pil
from ._distance import _distance_label

LPIPS_THRESHOLDS: list[tuple[float, str]] = [
    (0.10, "exact"),
    (0.30, "very similar"),
    (0.45, "similar"),
    (0.70, "different"),
    (0.90, "very different"),
    (float("inf"), "opposite"),
]


class ImgUtilsLPIPS(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLPIPS", display_name="Imgutils Compare (LPIPS)",
            category="imgutils/compare",
            description="Compute LPIPS perceptual similarity between two images. Lower = more similar.",
            search_aliases=["compare", "lpips", "perceptual", "similarity", "distance"],
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
        from imgutils.metrics import lpips_difference

        pil_a = comfy_to_pil(image_a)
        pil_b = comfy_to_pil(image_b)
        distance = lpips_difference(pil_a, pil_b)
        label = _distance_label(distance, LPIPS_THRESHOLDS)
        return io.NodeOutput(label, distance)
