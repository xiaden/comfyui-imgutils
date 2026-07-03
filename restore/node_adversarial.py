"""Node: ImgUtilsAdversarial — Adversarial noise removal."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsAdversarial(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsAdversarial", display_name="Imgutils Restore (Adversarial)",
            category="imgutils/restore",
            description="Remove adversarial noise using bilateral + guided filtering. No ML model needed.",
            search_aliases=["restore", "adversarial", "denoise", "noise", "clean", "mist"],
            inputs=[
                io.Image.Input("image", tooltip="Input image with adversarial noise"),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image) -> io.NodeOutput:
        from imgutils.restore import remove_adversarial_noise
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = remove_adversarial_noise(pil)
        return io.NodeOutput(pil_to_comfy(result))
