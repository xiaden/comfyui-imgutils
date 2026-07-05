"""Auto-crop image to visible content via transparency thresholding."""

from comfy_api.latest import io

from .._shared.bases import _ImageToImage


class ImgUtilsSqueeze(_ImageToImage):
    """Auto-crop image to visible content using transparency threshold."""
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsSqueeze", display_name="Imgutils Squeeze",
            category="imgutils/transform",
            description="Auto-crop image to visible content using transparency threshold.",
            search_aliases=["squeeze", "crop", "trim", "auto-crop", "transparency"],
            inputs=[
                io.Image.Input("image", tooltip="Input image with transparent regions."),
                io.Float.Input("threshold", default=0.7, min=0.0, max=1.0, step=0.05, tooltip="Transparency threshold for crop."),
                io.Int.Input("median_filter", default=5, min=0, max=15, step=1, tooltip="Median filter size for mask smoothing."),
            ],
            outputs=[io.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(cls, image, threshold, median_filter) -> io.NodeOutput:
        from imgutils.operate import squeeze_with_transparency
        mf = median_filter if median_filter > 0 else None
        return cls._run(image, squeeze_with_transparency, threshold=threshold, median_filter=mf)
