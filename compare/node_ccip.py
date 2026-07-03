"""Node: ImgUtilsCCIP — CCIP character similarity comparison."""
from __future__ import annotations
from comfy_api.latest import io
from ..utils import comfy_to_pil

class ImgUtilsCCIP(io.ComfyNode):
    OPS = ["ccip_difference", "ccip_same"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCCIP", display_name="Imgutils Compare (CCIP)",
            category="imgutils/compare",
            description="Compare anime character identity using CCIP. Outputs similarity distance or same-character check.",
            search_aliases=["compare", "ccip", "character", "similarity", "distance"],
            inputs=[
                io.Image.Input("image_a", tooltip="First image"),
                io.Image.Input("image_b", tooltip="Second image"),
                io.Combo.Input("operation", options=cls.OPS, default="ccip_difference", tooltip="CCIP comparison mode."),
            ],
            outputs=[io.String.Output(display_name="text")],
        )

    @classmethod
    def execute(cls, image_a, image_b, operation) -> io.NodeOutput:
        from imgutils.metrics import ccip_difference, ccip_same
        pil_a = comfy_to_pil(image_a.numpy() if hasattr(image_a, "numpy") else image_a)
        pil_b = comfy_to_pil(image_b.numpy() if hasattr(image_b, "numpy") else image_b)

        if operation == "ccip_difference":
            result = ccip_difference(pil_a, pil_b)
            return io.NodeOutput(f"CCIP distance: {result:.4f} (lower = more similar)")
        else:
            result = ccip_same(pil_a, pil_b)
            return io.NodeOutput(f"Same character: {'true' if result else 'false'}")
