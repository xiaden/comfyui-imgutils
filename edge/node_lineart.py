"""Neural lineart edge detection."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsLineart(_ImageToImage):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLineart", display_name="Imgutils Edge (Lineart)",
            category="imgutils/edge",
            description="Extract lineart edges using a neural lineart model.",
            search_aliases=["edge", "lineart", "outline", "line", "sketch"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to detect edges."),
                io.Boolean.Input("coarse", default=False, tooltip="Use coarse model for deeper/richer lines."),
                io.Int.Input("detect_resolution", default=512, min=128, max=2048, step=64, tooltip="Detection resolution."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, coarse, detect_resolution) -> io.NodeOutput:
        from imgutils.edge import edge_image_with_lineart
        return cls._run(image, edge_image_with_lineart, coarse=coarse, detect_resolution=detect_resolution)
