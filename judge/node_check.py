"""Boolean image property checks — AI-created, monochrome, greyscale, truncation, completeness."""

import json
import os
import tempfile

from comfy_api.latest import io
from .._shared.tensor import comfy_to_pil

class ImgUtilsCheck(io.ComfyNode):
    OPS = ["Is AI Created", "Is Monochrome", "Is Greyscale", "Is Truncated", "Anime Completeness"]

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsCheck", display_name="Imgutils Check",
            category="imgutils/judge",
            description="Boolean checks — AI-created detection, monochrome, greyscale, truncation, completeness.",
            search_aliases=["check", "boolean", "ai", "monochrome", "greyscale", "truncated", "completeness"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to analyze."),
                io.Combo.Input("mode", options=cls.OPS, default="Is AI Created", tooltip="What to check — AI-created detection, monochrome, greyscale, truncation, or completeness."),
            ],
            outputs=[
                io.String.Output(display_name="label"),
                io.Boolean.Output(display_name="boolean"),
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, mode) -> io.NodeOutput:
        from imgutils.validate import is_ai_created, is_monochrome, is_greyscale, is_truncated_file, anime_completeness

        pil = comfy_to_pil(image)

        if mode == "Is Truncated":
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                pil.save(tmp, format="PNG")
            tmp_path = tmp.name
            try:
                result = is_truncated_file(tmp_path)
            finally:
                os.unlink(tmp_path)
        else:
            funcs = {
                "Is AI Created": is_ai_created,
                "Is Monochrome": is_monochrome,
                "Is Greyscale": is_greyscale,
                "Anime Completeness": anime_completeness,
            }
            result = funcs[mode](pil)

        label = _check_label(mode, result)
        return io.NodeOutput(label, result, json.dumps({"result": result, "mode": mode}))


_CHECK_LABELS = {
    "Is AI Created": ("AI Created", "Not AI Created"),
    "Is Monochrome": ("Monochrome", "Not Monochrome"),
    "Is Greyscale": ("Greyscale", "Not Greyscale"),
    "Is Truncated": ("Truncated", "Not Truncated"),
    "Anime Completeness": ("Complete", "Incomplete"),
}


def _check_label(mode: str, result: bool) -> str:
    labels = _CHECK_LABELS.get(mode, ("true", "false"))
    return labels[0] if result else labels[1]
