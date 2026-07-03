"""Node: ImgUtilsCensor — NSFW content censoring."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsCensor(io.ComfyNode):
    METHODS = ["pixelate", "blur", "color"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCensor", display_name="Imgutils Censor",
            category="imgutils/transform",
            description="Auto-detect and censor NSFW content. Applies pixelation, blur, or solid color.",
            search_aliases=["censor", "nsfw", "pixelate", "blur", "mosaic"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Combo.Input("method", options=cls.METHODS, default="pixelate", tooltip="Censoring method."),
                io.Boolean.Input("nipple_f", default=True, tooltip="Censor female nipples."),
                io.Boolean.Input("penis", default=True, tooltip="Censor penises."),
                io.Boolean.Input("pussy", default=True, tooltip="Censor vaginas."),
                io.Float.Input("conf_threshold", default=0.3, min=0.0, max=1.0, step=0.05, tooltip="Detection confidence threshold."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, method, nipple_f, penis, pussy, conf_threshold) -> io.NodeOutput:
        from imgutils.operate import censor_nsfw
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = censor_nsfw(pil, method=str(method), nipple_f=bool(nipple_f), penis=bool(penis),
                             pussy=bool(pussy), conf_threshold=float(conf_threshold))
        return io.NodeOutput(pil_to_comfy(result))
