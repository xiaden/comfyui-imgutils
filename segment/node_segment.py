"""Anime character segmentation (background removal) using isnetis."""

from comfy_api.latest import io, ui

from .._shared.tensor import comfy_to_pil, pil_to_comfy


class ImgUtilsSegment(io.ComfyNode):
    """Segment anime character from background — outputs mask + RGBA."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsSegment",
            display_name="Imgutils Segment",
            category="imgutils/segment",
            description=(
                "Segment anime character from background using isnetis. "
                "Outputs the alpha mask and an RGBA image with transparent background."
            ),
            search_aliases=[
                "segment", "isnetis", "mask", "character",
                "background", "remove bg", "cutout", "alpha",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image containing character to segment."),
                io.Int.Input(
                    "scale", default=1024, min=256, max=2048, step=128,
                    tooltip="Processing resolution. Higher = more accurate, slower. Default 1024.",
                ),
            ],
            outputs=[
                io.Mask.Output(display_name="mask"),
                io.Image.Output(display_name="image"),
            ],
        )

    @classmethod
    def execute(cls, image, scale=1024) -> io.NodeOutput:
        from imgutils.segment import segment_rgba_with_isnetis

        pil_image = comfy_to_pil(image)

        mask_pil, rgba_pil = segment_rgba_with_isnetis(pil_image, scale=scale)

        mask_tensor = pil_to_comfy(mask_pil)
        rgba_tensor = pil_to_comfy(rgba_pil)

        return io.NodeOutput(mask_tensor, rgba_tensor, ui=ui.PreviewImage(rgba_tensor, cls=cls))
