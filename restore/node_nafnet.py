"""Node: ImgUtilsNAFNet — NAFNet image restoration."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsNAFNet(io.ComfyNode):
    MODELS = ["REDS", "GoPro", "SIDD"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsNAFNet", display_name="Imgutils Restore (NAFNet)",
            category="imgutils/restore",
            description="Restore/de-blur images using NAFNet. Note: may struggle with Gaussian noise.",
            search_aliases=["restore", "nafnet", "deblur", "clean", "enhance"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Combo.Input("model", options=cls.MODELS, default="REDS", tooltip="NAFNet model: REDS, GoPro, or SIDD."),
                io.Int.Input("tile_size", default=256, min=64, max=512, step=64, tooltip="Processing tile size."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, model, tile_size) -> io.NodeOutput:
        from imgutils.restore import restore_with_nafnet
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = restore_with_nafnet(pil, model=str(model), tile_size=int(tile_size))
        return io.NodeOutput(pil_to_comfy(result))
