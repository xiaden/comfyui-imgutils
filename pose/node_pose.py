"""Human pose keypoint detection and visualization using DWPose."""

from comfy_api.latest import io, ui

from .._shared.tensor import comfy_to_pil, pil_to_comfy
from .._shared.formatting import keypoints_to_json


class ImgUtilsPose(io.ComfyNode):
    """Detect OpenPose keypoints via DWPose and render skeleton visualization."""

    VISUALIZATION_PRESETS = [
        "Body Only",
        "Body with Face",
        "Body with Hands",
        "Full",
    ]

    PRESET_FLAGS = {
        "Body Only": {"draw_body": True, "draw_hands": False, "draw_feet": False, "draw_face": False},
        "Body with Face": {"draw_body": True, "draw_hands": False, "draw_feet": False, "draw_face": True},
        "Body with Hands": {"draw_body": True, "draw_hands": True, "draw_feet": False, "draw_face": False},
        "Full": {"draw_body": True, "draw_hands": True, "draw_feet": True, "draw_face": True},
    }

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsPose",
            display_name="Imgutils Pose",
            category="imgutils/pose",
            description=(
                "Detect OpenPose 18-point human keypoints in anime images "
                "using DWPose. Outputs a visualization image and keypoints JSON."
            ),
            search_aliases=[
                "pose", "keypoints", "dwpose", "skeleton", "openpose",
                "body", "face", "hands", "feet",
            ],
            inputs=[
                io.Image.Input("image", tooltip="Input image for pose detection."),
                io.Combo.Input(
                    "mode",
                    options=cls.VISUALIZATION_PRESETS,
                    default="Full",
                    tooltip="Visualization detail: body only, body+face, body+hands, or full skeleton.",
                ),
                io.Boolean.Input(
                    "auto_detect", default=True,
                    tooltip="Auto-detect person bounding boxes. Disable to use full image.",
                ),
            ],
            outputs=[
                io.Image.Output(display_name="skeleton"),
                io.String.Output(display_name="json"),
            ],
        )

    @classmethod
    def execute(cls, image, mode, auto_detect=True) -> io.NodeOutput:
        from imgutils.pose import dwpose_estimate, op18_visualize

        pil_image = comfy_to_pil(image)

        keypoints_list = dwpose_estimate(pil_image, auto_detect=auto_detect)
        json_str = keypoints_to_json(keypoints_list)
        flags = cls.PRESET_FLAGS.get(mode, cls.PRESET_FLAGS["Full"])
        vis_image = op18_visualize(
            pil_image,
            keypoints_list,
            draw_body=flags["draw_body"],
            draw_hands=flags["draw_hands"],
            draw_feet=flags["draw_feet"],
            draw_face=flags["draw_face"],
        )

        vis_tensor = pil_to_comfy(vis_image)
        return io.NodeOutput(vis_tensor, json_str, ui=ui.PreviewImage(vis_tensor, cls=cls))
