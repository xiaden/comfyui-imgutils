"""
Node 3: ImgUtilsTransform — "Do something"

Routes a dropdown to imgutils edge, restore, operate, and upscale functions.
All return PIL Images converted to ComfyUI IMAGE tensors.

Dropdown options (11):
  edge_image_with_canny        -> imgutils.edge.canny.edge_image_with_canny()
  edge_image_with_lineart      -> imgutils.edge.lineart.edge_image_with_lineart()
  edge_image_with_lineart_anime -> imgutils.edge.lineart_anime.edge_image_with_lineart_anime()
  restore_with_scunet          -> imgutils.restore.scunet.restore_with_scunet()
  restore_with_nafnet          -> imgutils.restore.nafnet.restore_with_nafnet()
  remove_adversarial_noise     -> imgutils.restore.adversarial.remove_adversarial_noise()
  upscale_with_cdc             -> imgutils.upscale.cdc.upscale_with_cdc()
  censor_nsfw                  -> imgutils.operate.censor_.censor_nsfw()
  censor_areas                 -> imgutils.operate.censor_.censor_areas()
  align_maxsize                -> imgutils.operate.align.align_maxsize()
  squeeze_with_transparency    -> imgutils.operate.squeeze_with_transparency()
"""

from __future__ import annotations

from comfy_api.latest import io, ui

from .utils import comfy_to_pil, pil_to_comfy


class ImgUtilsTransform(io.ComfyNode):
    """Transform an image using imgutils edge detection, restoration, and operations."""

    DROPDOWN_OPTIONS = [
        "edge_image_with_canny",
        "edge_image_with_lineart (~17 MB)",
        "edge_image_with_lineart_anime (~208 MB)",
        "restore_with_scunet (~87 MB)",
        "restore_with_nafnet (~263 MB)",
        "remove_adversarial_noise (~263 MB)",
        "upscale_with_cdc (~153 MB)",
        "censor_nsfw (~10 MB)",
        "censor_areas",
        "align_maxsize",
        "squeeze_with_transparency",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsTransform",
            display_name="Imgutils Transform",
            category="imgutils/transform",
            description=(
                "Transform anime images — Canny/Lineart edge detection, "
                "SCUNet/NAFNet restoration, adversarial noise removal, "
                 "CDC upscaling, NSFW censoring, image alignment, and transparency-aware squeeze."
            ),
            search_aliases=[
                "transform", "edge", "canny", "lineart", "restore",
                "scunet", "nafnet", "upscale", "cdc", "censor",
                "nsfw", "align", "squeeze", "denoise", "transparency",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to transform"),
                io.Combo.Input(
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="edge_image_with_canny",
                    tooltip="Select transformation: Canny/Lineart edge detection, restoration, upscaling, NSFW censoring, alignment, or transparency-based squeeze.",
                ),
            ],
            outputs=[
                io.Image.Output(display_name="image"),
            ],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        """
        Route the operation to the correct imgutils function.

        Args:
            image: ComfyUI IMAGE tensor (B,H,W,C), float32, [0,1]
            operation: dropdown selection

        Returns:
            NodeOutput with (IMAGE_tensor,)
        """
        operation = operation.split(" (")[0]  # strip size annotation

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        # ---- Edge detection ----
        if operation == "edge_image_with_canny":
            from imgutils.edge import edge_image_with_canny

            result = edge_image_with_canny(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "edge_image_with_lineart":
            from imgutils.edge import edge_image_with_lineart

            result = edge_image_with_lineart(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "edge_image_with_lineart_anime":
            from imgutils.edge import edge_image_with_lineart_anime

            result = edge_image_with_lineart_anime(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        # ---- Restore ----
        elif operation == "restore_with_scunet":
            from imgutils.restore import restore_with_scunet

            result = restore_with_scunet(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "restore_with_nafnet":
            from imgutils.restore import restore_with_nafnet

            result = restore_with_nafnet(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "remove_adversarial_noise":
            from imgutils.restore import remove_adversarial_noise

            result = remove_adversarial_noise(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        # ---- Upscale ----
        elif operation == "upscale_with_cdc":
            from imgutils.upscale import upscale_with_cdc

            result = upscale_with_cdc(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        # ---- Operate ----
        elif operation == "censor_nsfw":
            from imgutils.operate import censor_nsfw

            result = censor_nsfw(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "censor_areas":
            from imgutils.operate import censor_areas

            result = censor_areas(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "align_maxsize":
            from imgutils.operate import align_maxsize

            result = align_maxsize(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        elif operation == "squeeze_with_transparency":
            from imgutils.operate import squeeze_with_transparency

            result = squeeze_with_transparency(pil_image)
            out = pil_to_comfy(result)
            return io.NodeOutput(out, ui=ui.PreviewImage(out, cls=cls))

        else:
            # Unknown operation — return input unchanged
            return io.NodeOutput(image, ui=ui.PreviewImage(image, cls=cls))
