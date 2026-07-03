"""Node: ImgUtilsLineart — Lineart edge detection."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsLineart(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLineart", display_name="Imgutils Edge (Lineart)",
            category="imgutils/edge",
            description="Extract lineart edges using a neural lineart model. Best quality, higher resource usage.",
            search_aliases=["edge", "lineart", "outline", "line", "sketch"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Boolean.Input("coarse", default=False, tooltip="Use coarse model for deeper/richer lines."),
                io.Int.Input("detect_resolution", default=512, min=128, max=2048, step=64, tooltip="Detection resolution."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, coarse, detect_resolution) -> io.NodeOutput:
        from imgutils.edge import edge_image_with_lineart
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = edge_image_with_lineart(pil, coarse=bool(coarse), detect_resolution=int(detect_resolution))
        return io.NodeOutput(pil_to_comfy(result))
