"""Node: ImgUtilsCheck — Boolean image property checks."""
from __future__ import annotations
import os, tempfile
from comfy_api.latest import io
from ..utils import comfy_to_pil

class ImgUtilsCheck(io.ComfyNode):
    OPS = ["is_ai_created", "is_monochrome", "is_greyscale", "is_truncated", "anime_completeness"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCheck", display_name="Imgutils Check",
            category="imgutils/validate",
            description="Boolean checks — AI-created detection, monochrome, greyscale, truncation, completeness.",
            search_aliases=["check", "boolean", "ai", "monochrome", "greyscale", "truncated", "completeness"],
            inputs=[
                io.Image.Input("image", tooltip="Input image"),
                io.Combo.Input("operation", options=cls.OPS, default="is_ai_created", tooltip="Check type."),
            ],
            outputs=[io.String.Output(display_name="result"), io.String.Output(display_name="detail")],
        )

    @classmethod
    def execute(cls, image, operation) -> io.NodeOutput:
        from imgutils.validate import is_ai_created, is_monochrome, is_greyscale, is_truncated_file, anime_completeness

        pil = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        if operation == "is_truncated":
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                pil.save(tmp, format="PNG"); tmp_path = tmp.name
            try:
                result = is_truncated_file(tmp_path)
            finally:
                os.unlink(tmp_path)
        else:
            funcs = {
                "is_ai_created": is_ai_created, "is_monochrome": is_monochrome,
                "is_greyscale": is_greyscale, "anime_completeness": anime_completeness,
            }
            result = funcs[operation](pil)

        return io.NodeOutput("true" if result else "false", str(result))
