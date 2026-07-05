"""Anime-optimized neural lineart edge detection."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsLineartAnime(_ImageToImage):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLineartAnime", display_name="Imgutils Edge (Lineart Anime)",
            category="imgutils/edge",
            description="Extract lineart edges optimized for anime images.",
            search_aliases=["edge", "lineart", "anime", "outline", "line", "sketch"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to detect anime edges."),
                io.Int.Input("detect_resolution", default=512, min=128, max=2048, step=64, tooltip="Detection resolution."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, detect_resolution) -> io.NodeOutput:
        from imgutils.edge import edge_image_with_lineart_anime
        return cls._run(image, edge_image_with_lineart_anime, detect_resolution=detect_resolution)
