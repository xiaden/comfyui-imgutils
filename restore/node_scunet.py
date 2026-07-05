"""SCUNet image restoration/de-noising."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsSCUNet(_ImageToImage):
    MODELS = ["GAN", "PSNR"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsSCUNet", display_name="Imgutils Restore (SCUNet)",
            category="imgutils/restore",
            description="Restore/de-noise images using SCUNet.",
            search_aliases=["restore", "scunet", "denoise", "clean", "enhance"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to restore/denoise."),
                io.Combo.Input("mode", options=cls.MODELS, default="GAN", tooltip="SCUNet model variant: GAN or PSNR."),
                io.Int.Input("tile_size", default=128, min=64, max=512, step=64, tooltip="Processing tile size. Larger = more VRAM."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, mode, tile_size) -> io.NodeOutput:
        from imgutils.restore import restore_with_scunet
        return cls._run(image, restore_with_scunet, model=mode, tile_size=tile_size)
