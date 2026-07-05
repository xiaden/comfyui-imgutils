"""Canny edge detection."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsCanny(_ImageToImage):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCanny", display_name="Imgutils Edge (Canny)",
            category="imgutils/edge",
            description="Extract edges using Canny edge detection.",
            search_aliases=["edge", "canny", "outline", "line", "sketch"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to detect edges."),
                io.Int.Input("low_threshold", default=100, min=0, max=500, step=10, tooltip="Canny low threshold."),
                io.Int.Input("high_threshold", default=200, min=0, max=500, step=10, tooltip="Canny high threshold."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, low_threshold, high_threshold) -> io.NodeOutput:
        from imgutils.edge import edge_image_with_canny
        return cls._run(image, edge_image_with_canny, low_threshold=low_threshold, high_threshold=high_threshold)
