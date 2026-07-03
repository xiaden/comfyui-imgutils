"""Node: ImgUtilsCanny — Canny edge detection."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsCanny(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCanny", display_name="Imgutils Edge (Canny)",
            category="imgutils/edge",
            description="Extract edges using Canny edge detection. Fastest edge method.",
            search_aliases=["edge", "canny", "outline", "line", "sketch"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Int.Input("low_threshold", default=100, min=0, max=500, step=10, tooltip="Canny low threshold."),
                io.Int.Input("high_threshold", default=200, min=0, max=500, step=10, tooltip="Canny high threshold."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, low_threshold, high_threshold) -> io.NodeOutput:
        from imgutils.edge import edge_image_with_canny
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = edge_image_with_canny(pil, low_threshold=int(low_threshold), high_threshold=int(high_threshold))
        return io.NodeOutput(pil_to_comfy(result))
