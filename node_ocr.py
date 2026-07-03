"""
Node: ImgUtilsOCR — Optical character recognition.

Extracts text from images using PaddleOCR through imgutils.
"""

from __future__ import annotations

from comfy_api.latest import io

from ..utils import comfy_to_pil


class ImgUtilsOCR(io.ComfyNode):
    """Optical character recognition for anime images."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsOCR",
            display_name="Imgutils OCR",
            category="imgutils/describe",
            description=(
                "Extract text from images using PaddleOCR. "
                "Returns recognized text strings and text with confidence scores."
            ),
            search_aliases=[
                "ocr", "text", "recognize", "read", "paddleocr", "extract",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image to extract text from"),
                io.Float.Input(
                    "heat_threshold", default=0.3, min=0.0, max=1.0, step=0.05,
                    tooltip="Heat map threshold for text region detection. Lower = more regions.",
                ),
                io.Float.Input(
                    "box_threshold", default=0.7, min=0.0, max=1.0, step=0.05,
                    tooltip="Box threshold for text detection. Lower = more candidate boxes.",
                ),
            ],
            outputs=[
                io.String.Output(display_name="text"),
                io.String.Output(display_name="scores"),
            ],
        )

    @classmethod
    def execute(cls, image, heat_threshold, box_threshold) -> io.NodeOutput:
        from imgutils.ocr import ocr

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)
        results = ocr(
            pil_image,
            heat_threshold=float(heat_threshold),
            box_threshold=float(box_threshold),
        )

        if not results:
            return io.NodeOutput("No text detected.", "No text detected.")

        text_strs = [text for bbox, text, conf in results]
        text_only = ", ".join(f'"{t}"' for t in text_strs)
        text_scores = "\n".join(
            f"  [{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}] \"{text}\" ({conf:.4f})"
            for bbox, text, conf in results
        )
        return io.NodeOutput(text_only, text_scores)
