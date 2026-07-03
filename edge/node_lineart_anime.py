"""Node: ImgUtilsLineartAnime — Anime-optimized lineart edge detection."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil, pil_to_comfy

class ImgUtilsLineartAnime(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsLineartAnime", display_name="Imgutils Edge (Lineart Anime)",
            category="imgutils/edge",
            description="Extract lineart edges optimized for anime images.",
            search_aliases=["edge", "lineart", "anime", "outline", "line", "sketch"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Int.Input("detect_resolution", default=512, min=128, max=2048, step=64, tooltip="Detection resolution."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, detect_resolution) -> io.NodeOutput:
        from imgutils.edge import edge_image_with_lineart_anime
        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        result = edge_image_with_lineart_anime(pil, detect_resolution=int(detect_resolution))
        return io.NodeOutput(pil_to_comfy(result))
