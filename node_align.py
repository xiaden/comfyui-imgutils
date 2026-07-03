"""Node: ImgUtilsAlign — Resize image to max dimension."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsAlign(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsAlign", display_name="Imgutils Align",
            category="imgutils/transform",
            description="Resize image so its longest side matches max_size, preserving aspect ratio.",
            search_aliases=["align", "resize", "max", "fit", "scale"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Int.Input("max_size", default=1024, min=64, max=8192, step=64, tooltip="Maximum side length."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, max_size) -> io.NodeOutput:
        from imgutils.operate import align_maxsize
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = align_maxsize(pil, max_size=int(max_size))
        return io.NodeOutput(pil_to_comfy(result))
