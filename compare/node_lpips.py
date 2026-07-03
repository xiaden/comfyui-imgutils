"""Node: ImgUtilsLPIPS — LPIPS perceptual similarity."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil

class ImgUtilsLPIPS(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLPIPS", display_name="Imgutils Compare (LPIPS)",
            category="imgutils/compare",
            description="Compute LPIPS perceptual similarity between two images. Score < 0.45 = similar.",
            search_aliases=["compare", "lpips", "perceptual", "similarity", "distance"],
            inputs=[
                io.Image.Input("image_a", tooltip="First image"),
                io.Image.Input("image_b", tooltip="Second image"),
            ],
            outputs=[io.String.Output(display_name="text")],
        )

    @classmethod
    def execute(cls, image_a, image_b) -> io.NodeOutput:
        from imgutils.metrics import lpips_difference
        pil_a = comfy_to_pil(image_a.numpy() if hasattr(image_a, "numpy") else image_a)
        pil_b = comfy_to_pil(image_b.numpy() if hasattr(image_b, "numpy") else image_b)
        result = lpips_difference(pil_a, pil_b)
        similar = result < 0.45
        return io.NodeOutput(f"LPIPS: {result:.4f} ({'similar' if similar else 'different'}, threshold=0.45)")
