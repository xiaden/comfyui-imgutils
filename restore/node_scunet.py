"""Node: ImgUtilsSCUNet — SCUNet image restoration."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsSCUNet(io.ComfyNode):
    MODELS = ["GAN", "PSNR"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsSCUNet", display_name="Imgutils Restore (SCUNet)",
            category="imgutils/restore",
            description="Restore/de-noise images using SCUNet.",
            search_aliases=["restore", "scunet", "denoise", "clean", "enhance"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Combo.Input("model", options=cls.MODELS, default="GAN", tooltip="SCUNet model: GAN or PSNR."),
                io.Int.Input("tile_size", default=128, min=64, max=512, step=64, tooltip="Processing tile size. Larger = more VRAM."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, model, tile_size) -> io.NodeOutput:
        from imgutils.restore import restore_with_scunet
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = restore_with_scunet(pil, model=str(model), tile_size=int(tile_size))
        return io.NodeOutput(pil_to_comfy(result))
