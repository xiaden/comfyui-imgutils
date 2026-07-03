"""
Node 6: ImgUtilsSegment — "Segment character"

Segments character from background using isnetis (anime character segmentation).
Outputs both a mask image and the segmented RGBA image with transparent background.

Uses:
  imgutils.segment.isnetis.segment_rgba_with_isnetis() -> (mask: PIL, rgba_image: PIL)
"""

from __future__ import annotations

from comfy_api.latest import io, ui

from .utils import comfy_to_pil, pil_to_comfy


class ImgUtilsSegment(io.ComfyNode):
    """Segment character from background using isnetis."""

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
                io.Image.Input("image", tooltip="Input image containing character to segment"),
                io.Int.Input(
                    "scale", default=1024, min=256, max=2048, step=128,
                    tooltip="Processing resolution. Higher = more accurate, slower. Default 1024.",
                ),
            ],
            outputs=[
                io.Mask.Output(display_name="mask"),
                io.Image.Output(display_name="segmented_rgba"),
            ],
        )

    @classmethod
    def execute(cls, image, scale=1024) -> io.NodeOutput:
        """
        Run character segmentation and return mask + RGBA image.

        Args:
            image: ComfyUI IMAGE tensor (B,H,W,C), float32, [0,1]

        Returns:
            NodeOutput with (mask_tensor, segmented_rgba_tensor)
        """
        from imgutils.segment import segment_rgba_with_isnetis

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        mask_pil, rgba_pil = segment_rgba_with_isnetis(pil_image, scale=int(scale))

        # pil_to_comfy handles grayscale "L" mode (mask) and "RGBA" mode
        mask_tensor = pil_to_comfy(mask_pil)
        rgba_tensor = pil_to_comfy(rgba_pil)

        return io.NodeOutput(mask_tensor, rgba_tensor, ui=ui.PreviewImage(rgba_tensor, cls=cls))
