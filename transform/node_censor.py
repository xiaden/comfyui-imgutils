"""NSFW content auto-censoring — pixelate, blur, or color-fill detected regions."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsCensor(_ImageToImage):
    """Detect and censor NSFW regions using pixelation, blur, or solid color fills."""
    METHODS = ["Pixelate", "Blur", "Color"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCensor", display_name="Imgutils Censor",
            category="imgutils/transform",
            description="Auto-detect and censor NSFW content. Applies pixelation, blur, or solid color.",
            search_aliases=["censor", "nsfw", "pixelate", "blur", "mosaic"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to censor NSFW content."),
                io.Combo.Input("mode", options=cls.METHODS, default="Pixelate", tooltip="Censoring method."),
                io.Boolean.Input("nipple_f", default=True, tooltip="Censor female nipples."),
                io.Boolean.Input("penis", default=True, tooltip="Censor penises."),
                io.Boolean.Input("pussy", default=True, tooltip="Censor vaginas."),
                io.Float.Input("confidence", default=0.3, min=0.0, max=1.0, step=0.05, tooltip="Detection confidence threshold."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, mode, nipple_f, penis, pussy, confidence) -> io.NodeOutput:
        from imgutils.operate import censor_nsfw
        return cls._run(image, censor_nsfw, method=mode.lower(), nipple_f=nipple_f,
                        penis=penis, pussy=pussy, conf_threshold=confidence)
