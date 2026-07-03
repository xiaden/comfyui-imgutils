"""Node: ImgUtilsSqueeze — Crop to visible content using transparency."""
from __future__ import annotations
from comfy_api.latest import io
from .utils import comfy_to_pil, pil_to_comfy

class ImgUtilsSqueeze(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsSqueeze", display_name="Imgutils Squeeze",
            category="imgutils/transform",
            description="Auto-crop image to visible content using transparency threshold.",
            search_aliases=["squeeze", "crop", "trim", "auto-crop", "transparency"],
            inputs=[
                io.Image.Input("image", tooltip="Input image with transparent regions"),
                io.Float.Input("threshold", default=0.7, min=0.0, max=1.0, step=0.05, tooltip="Transparency threshold for crop."),
                io.Int.Input("median_filter", default=5, min=0, max=15, step=1, tooltip="Median filter size for mask smoothing."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, threshold, median_filter) -> io.NodeOutput:
        from imgutils.operate import squeeze_with_transparency
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        mf = int(median_filter) if int(median_filter) > 0 else None
        result = squeeze_with_transparency(pil, threshold=float(threshold), median_filter=mf)
        return io.NodeOutput(pil_to_comfy(result))
