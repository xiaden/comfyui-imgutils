"""Crop image to each bounding box from detect/OCR JSON output."""

import json
from comfy_api.latest import io, ui
from .._shared.tensor import comfy_to_pil, pil_to_comfy


class ImgUtilsBboxCrop(io.ComfyNode):
    """Crop an image into one sub-image per bounding box from detect/OCR results."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsBboxCrop",
            display_name="Imgutils Bbox Crop",
            category="imgutils/utility",
            description=(
                "Crop an image to each bounding box in a JSON bbox string "
                "(from Detect or OCR). Returns one cropped image per bbox."
            ),
            search_aliases=["bbox", "crop", "detect", "region", "extract"],
            inputs=[
                io.Image.Input("image", tooltip="Source image for cropping."),
                io.String.Input(
                    "bboxes",
                    tooltip="JSON bbox array from Detect or OCR node. Each entry: {bbox: [x1,y1,x2,y2], ...}.",
                ),
            ],
            outputs=[io.Image.Output(display_name="images", is_output_list=True)],
        )

    @classmethod
    def execute(cls, image, bboxes) -> io.NodeOutput:
        pil = comfy_to_pil(image)
        w, h = pil.size

        try:
            entries = json.loads(bboxes)
        except json.JSONDecodeError:
            entries = []

        crops: list = []
        for entry in entries:
            bbox = entry.get("bbox", entry)
            if isinstance(bbox, list) and len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                x1 = max(0, min(int(x1), w - 1))
                y1 = max(0, min(int(y1), h - 1))
                x2 = max(x1 + 1, min(int(x2), w))
                y2 = max(y1 + 1, min(int(y2), h))
                crop = pil.crop((x1, y1, x2, y2))
                crops.append(pil_to_comfy(crop))

        if not crops:
            return io.NodeOutput([pil_to_comfy(pil)])

        return io.NodeOutput(
            crops,
            ui=ui.PreviewImage(crops[0], cls=cls),
        )
