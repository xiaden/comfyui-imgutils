"""OCR text extraction from anime images via PaddleOCR."""

import json

from comfy_api.latest import io

from .._shared.tensor import comfy_to_pil


class ImgUtilsOCR(io.ComfyNode):
    """Extract text from anime images using PaddleOCR."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsOCR",
            display_name="Imgutils OCR",
            category="imgutils/ocr",
            description=(
                "Extract text from images using PaddleOCR. "
                "Returns recognized text strings and text with confidence scores."
            ),
            search_aliases=[
                "ocr", "text", "recognize", "read", "paddleocr", "extract",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image for text extraction."),
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
                io.String.Output(display_name="detections"),
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, heat_threshold, box_threshold) -> io.NodeOutput:
        from imgutils.ocr import ocr

        pil_image = comfy_to_pil(image)
        results = ocr(
            pil_image,
            heat_threshold=heat_threshold,
            box_threshold=box_threshold,
        )

        if not results:
            return io.NodeOutput("No text detected.", "[]")

        text_strs = [text for bbox, text, conf in results]
        text_only = ", ".join(f'"{t}"' for t in text_strs)
        bboxes_json = json.dumps([
            {"bbox": [bbox[0], bbox[1], bbox[2], bbox[3]], "label": text, "score": conf}
            for bbox, text, conf in results
        ], ensure_ascii=False)
        return io.NodeOutput(text_only, bboxes_json)
