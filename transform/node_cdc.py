"""CDC-based anime image upscaling (high quality, slow)."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsCDC(_ImageToImage):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCDC", display_name="Imgutils Upscale (CDC)",
            category="imgutils/transform",
            description="High-quality anime upscaling using CDC model. Slow but excellent quality.",
            search_aliases=["upscale", "cdc", "anime", "enlarge", "4x"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to upscale."),
                io.Int.Input("tile_size", default=512, min=128, max=1024, step=64, tooltip="Processing tile size."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, tile_size) -> io.NodeOutput:
        from imgutils.upscale import upscale_with_cdc
        return cls._run(image, upscale_with_cdc, tile_size=tile_size)
