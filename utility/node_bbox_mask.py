"""Create binary masks from bounding box JSON data."""

import json
import numpy as np
import torch
from comfy_api.latest import io


class ImgUtilsBboxMask(io.ComfyNode):
    """Create binary masks — one per bounding box from detect/OCR results."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsBboxMask",
            display_name="Imgutils Bbox Mask",
            category="imgutils/utility",
            description=(
                "Create binary masks from JSON bounding box data "
                "(from Detect or OCR). Returns one mask per bbox."
            ),
            search_aliases=["bbox", "mask", "detect", "region", "crop"],
            inputs=[
                io.Image.Input("image", tooltip="Source image (used for dimensions)."),
                io.String.Input(
                    "bboxes",
                    tooltip="JSON bbox array from Detect or OCR node. Each entry: {bbox: [x1,y1,x2,y2], ...}.",
                ),
            ],
            outputs=[io.Mask.Output(display_name="masks", is_output_list=True)],
        )

    @classmethod
    def execute(cls, image, bboxes) -> io.NodeOutput:
        img = image.numpy()
        _, h, w, _ = img.shape

        try:
            entries = json.loads(bboxes)
        except json.JSONDecodeError:
            entries = []

        masks: list = []
        for entry in entries:
            bbox = entry.get("bbox", entry)
            if isinstance(bbox, list) and len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                x1 = max(0, min(int(x1), w - 1))
                y1 = max(0, min(int(y1), h - 1))
                x2 = max(x1 + 1, min(int(x2), w))
                y2 = max(y1 + 1, min(int(y2), h))

                mask = np.zeros((h, w), dtype=np.float32)
                mask[y1:y2, x1:x2] = 1.0
                masks.append(torch.from_numpy(mask).unsqueeze(0))

        if not masks:
            empty = torch.zeros((1, h, w), dtype=torch.float32)
            return io.NodeOutput([empty])

        return io.NodeOutput(masks)
