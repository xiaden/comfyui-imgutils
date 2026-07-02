"""
Node 5: ImgUtilsPose — "Detect pose"

Detects human keypoints in anime images using DWPose and visualizes them.
Outputs the visualization image and keypoints as JSON.

Visualization presets (mapped to op18_visualize flags):
  body_only        -> body=True,  hands=False, feet=False, face=False
  body_with_face   -> body=True,  hands=False, feet=False, face=True
  body_with_hands  -> body=True,  hands=True,  feet=False, face=False
  full             -> body=True,  hands=True,  feet=True,  face=True
"""

from __future__ import annotations

from comfy_api.latest import io, ui

from .utils import comfy_to_pil, pil_to_comfy, keypoints_to_json


class ImgUtilsPose(io.ComfyNode):
    """Detect human pose keypoints and visualize them."""

    VISUALIZATION_PRESETS = [
        "body_only",
        "body_with_face",
        "body_with_hands",
        "full",
    ]

    # Mapping from preset name to op18_visualize boolean flags
    PRESET_FLAGS = {
        "body_only":       {"draw_body": True,  "draw_hands": False, "draw_feet": False, "draw_face": False},
        "body_with_face":  {"draw_body": True,  "draw_hands": False, "draw_feet": False, "draw_face": True},
        "body_with_hands": {"draw_body": True,  "draw_hands": True,  "draw_feet": False, "draw_face": False},
        "full":            {"draw_body": True,  "draw_hands": True,  "draw_feet": True,  "draw_face": True},
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
                io.Image.Input("image", tooltip="Input image for pose detection"),
                io.Combo.Input(
                    "visualization",
                    options=cls.VISUALIZATION_PRESETS,
                    default="full",
                    tooltip="Visualization detail preset: body only, body+face, body+hands, or full (all keypoints).",
                ),
            ],
            outputs=[
                io.Image.Output(display_name="visualization"),
                io.String.Output(display_name="keypoints_json"),
            ],
        )

    @classmethod
    def execute(cls, image, visualization) -> io.NodeOutput:
        """
        Detect pose keypoints and render visualization.

        Args:
            image: ComfyUI IMAGE tensor (B,H,W,C), float32, [0,1]
            visualization: preset name for op18_visualize flags

        Returns:
            NodeOutput with (visualization_IMAGE, keypoints_json_STRING)
        """
        from imgutils.pose import dwpose_estimate, op18_visualize

        pil_image = comfy_to_pil(image.numpy() if hasattr(image, "numpy") else image)

        # Estimate keypoints
        keypoints_list = dwpose_estimate(pil_image)

        # Build JSON from keypoints
        json_str = keypoints_to_json(keypoints_list)

        # Visualize with selected preset
        flags = cls.PRESET_FLAGS.get(visualization, cls.PRESET_FLAGS["full"])
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
