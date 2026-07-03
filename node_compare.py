"""
Node 4: ImgUtilsCompare — "Compare images"

Compares two images using imgutils metrics functions.
Accepts two IMAGE inputs (A and B).

Dropdown options (3):
  ccip_difference  -> imgutils.metrics.ccip.ccip_difference() - character similarity distance
  ccip_same        -> imgutils.metrics.ccip.ccip_same()       - same character check
  lpips_difference -> imgutils.metrics.lpips.lpips_difference() - perceptual similarity
"""

from __future__ import annotations

from comfy_api.latest import io

from .utils import comfy_to_pil


class ImgUtilsCompare(io.ComfyNode):
    """Compare two images using imgutils metrics."""

    DROPDOWN_OPTIONS = [
        "ccip_difference (~143 MB)",
        "ccip_same",
        "lpips_difference (~10 MB)",
    ]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCompare",
            display_name="Imgutils Compare",
            category="imgutils/compare",
            description=(
                "Compare two images using CCIP character similarity distance, "
                "CCIP same-character check, or LPIPS perceptual similarity."
            ),
            search_aliases=[
                "compare", "ccip", "lpips", "similarity",
                "distance", "perceptual", "character",
            ],
            inputs=[
                io.Image.Input("image_a", tooltip="First image to compare"),
                io.Image.Input("image_b", tooltip="Second image to compare"),
                io.Combo.Input(
                    "operation",
                    options=cls.DROPDOWN_OPTIONS,
                    default="ccip_difference",
                    tooltip="Comparison method: CCIP character similarity distance, same-character check, or LPIPS perceptual similarity.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="text"),
            ],
        )

    @classmethod
    def execute(cls, image_a, image_b, operation) -> io.NodeOutput:
        """
        Route the operation to the correct imgutils comparison function.

        Args:
            image_a: first ComfyUI IMAGE tensor
            image_b: second ComfyUI IMAGE tensor
            operation: dropdown selection

        Returns:
            NodeOutput with (text_string,)
        """
        operation = operation.split(" (")[0]  # strip size annotation

        pil_a = comfy_to_pil(image_a.numpy() if hasattr(image_a, "numpy") else image_a)
        pil_b = comfy_to_pil(image_b.numpy() if hasattr(image_b, "numpy") else image_b)

        if operation == "ccip_difference":
            from imgutils.metrics import ccip_difference

            result = ccip_difference(pil_a, pil_b)
            return io.NodeOutput(f"CCIP distance: {result:.4f} (lower = more similar)")

        elif operation == "ccip_same":
            from imgutils.metrics import ccip_same

            result = ccip_same(pil_a, pil_b)
            return io.NodeOutput(f"Same character: {'true' if result else 'false'}")

        elif operation == "lpips_difference":
            from imgutils.metrics import lpips_difference

            result = lpips_difference(pil_a, pil_b)
            similar = result < 0.45
            return io.NodeOutput(
                f"LPIPS distance: {result:.4f} "
                f"({'similar' if similar else 'different'}, threshold=0.45)",
            )

        else:
            return io.NodeOutput(f"Unknown operation: {operation}")
