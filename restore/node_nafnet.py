"""NAFNet image restoration/de-blurring."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsNAFNet(_ImageToImage):
    MODELS = ["REDS", "GoPro", "SIDD"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsNAFNet", display_name="Imgutils Restore (NAFNet)",
            category="imgutils/restore",
            description="Restore/de-blur images using NAFNet. Note: may struggle with Gaussian noise.",
            search_aliases=["restore", "nafnet", "deblur", "clean", "enhance"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to restore/deblur."),
                io.Combo.Input("mode", options=cls.MODELS, default="REDS", tooltip="NAFNet model variant: REDS, GoPro, or SIDD."),
                io.Int.Input("tile_size", default=256, min=64, max=512, step=64, tooltip="Processing tile size."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, mode, tile_size) -> io.NodeOutput:
        from imgutils.restore import restore_with_nafnet
        return cls._run(image, restore_with_nafnet, model=mode, tile_size=tile_size)
