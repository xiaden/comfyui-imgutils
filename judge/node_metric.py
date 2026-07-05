"""Numeric image quality metrics — sharpness (Laplacian) and monochrome score."""

import json
from comfy_api.latest import io
from .._shared.tensor import comfy_to_pil

class ImgUtilsMetric(io.ComfyNode):
    OPS = ["Monochrome Score", "Laplacian Score"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsMetric", display_name="Imgutils Metric",
            category="imgutils/judge",
            description="Numeric image quality metrics — monochrome score and sharpness (Laplacian).",
            search_aliases=["metric", "score", "sharpness", "laplacian", "monochrome", "blur"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to measure quality."),
                io.Combo.Input("mode", options=cls.OPS, default="Laplacian Score", tooltip="Metric to compute — Laplacian sharpness score or monochrome ratio."),
            ],
            outputs=[
                io.String.Output(display_name="label"),
                io.Float.Output(display_name="score"),
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, mode) -> io.NodeOutput:
        from imgutils.metrics import laplacian_score
        from imgutils.validate import get_monochrome_score

        pil = comfy_to_pil(image)

        if mode == "Monochrome Score":
            v = get_monochrome_score(pil)
            label = f"{v:.4f}"
            score = v
        else:
            v = laplacian_score(pil)
            label = "sharp" if v >= 100 else "blurry"
            score = v

        return io.NodeOutput(label, score, json.dumps({"label": label, "score": score, "mode": mode}))
