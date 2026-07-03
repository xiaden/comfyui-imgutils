"""Node: ImgUtilsMetric — Numeric image quality metrics."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil

class ImgUtilsMetric(io.ComfyNode):
    OPS = ["monochrome_score", "laplacian_score"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsMetric", display_name="Imgutils Metric",
            category="imgutils/validate",
            description="Numeric image quality metrics — monochrome score and sharpness (Laplacian).",
            search_aliases=["metric", "score", "sharpness", "laplacian", "monochrome", "blur"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Combo.Input("operation", options=cls.OPS, default="laplacian_score", tooltip="Metric type."),
            ],
            outputs=[io.String.Output(display_name="label"), io.Float.Output(display_name="score")],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        from imgutils.metrics import laplacian_score
        from imgutils.validate import get_monochrome_score

        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        if operation == "monochrome_score":
            v = get_monochrome_score(pil)
            return io.NodeOutput(f"{v:.4f}", float(v))
        else:
            v = laplacian_score(pil)
            quality = "sharp" if v >= 100 else "blurry"
            return io.NodeOutput(quality, float(v))
