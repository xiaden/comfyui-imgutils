"""Resize image to a maximum dimension while preserving aspect ratio."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsAlign(_ImageToImage):
    """Resize image so longest side matches max_size, preserving aspect ratio."""
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsAlign", display_name="Imgutils Align",
            category="imgutils/transform",
            description="Resize image so its longest side matches max_size, preserving aspect ratio.",
            search_aliases=["align", "resize", "max", "fit", "scale"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to resize to max dimension."),
                io.Int.Input("max_size", default=1024, min=64, max=8192, step=64, tooltip="Maximum side length."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, max_size) -> io.NodeOutput:
        from imgutils.operate import align_maxsize
        return cls._run(image, align_maxsize, max_size=max_size)
