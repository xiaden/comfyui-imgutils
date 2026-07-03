"""Node: ImgUtilsCDC — CDC anime upscaling."""
from __future__ import annotations
from comfy_api.latest import io
from .utils import comfy_to_pil, pil_to_comfy

class ImgUtilsCDC(io.ComfyNode):
    MODELS = ["HGSR-MHR-anime-aug_X4_320"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCDC", display_name="Imgutils Upscale (CDC)",
            category="imgutils/transform",
            description="High-quality anime upscaling using CDC model. Slow but excellent quality.",
            search_aliases=["upscale", "cdc", "anime", "enlarge", "4x"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Int.Input("tile_size", default=512, min=128, max=1024, step=64, tooltip="Processing tile size."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, tile_size) -> io.NodeOutput:
        from imgutils.upscale import upscale_with_cdc
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = upscale_with_cdc(pil, tile_size=int(tile_size))
        return io.NodeOutput(pil_to_comfy(result))
