"""Adversarial noise removal using bilateral and guided filtering (no ML model)."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsAdversarial(_ImageToImage):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsAdversarial", display_name="Imgutils Restore (Adversarial)",
            category="imgutils/restore",
            description="Remove adversarial noise using bilateral + guided filtering. No ML model needed.",
            search_aliases=["restore", "adversarial", "denoise", "noise", "clean", "mist"],
            inputs=[
                io.Image.Input("image", tooltip="Input image to remove adversarial noise from."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image) -> io.NodeOutput:
        from imgutils.restore import remove_adversarial_noise
        return cls._run(image, remove_adversarial_noise)
