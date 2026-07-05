"""
Base classes for image-to-image transform nodes.
"""

from comfy_api.latest import io, ui

from .tensor import comfy_to_pil, pil_to_comfy


class _ImageToImage(io.ComfyNode):
    """Base for nodes that map one image to another via a PIL transform function.

    Subclasses call ``cls._run(image, func, **kwargs)`` in their ``execute``
    method, passing the PIL-level transform function and any kwargs it needs.
    """

    @classmethod
    def _run(cls, image, func, **kwargs):
        """Convert to PIL, apply func, convert back, return with preview."""
        pil = comfy_to_pil(image)
        result = func(pil, **kwargs)
        result_tensor = pil_to_comfy(result)
        return io.NodeOutput(result_tensor, ui=ui.PreviewImage(result_tensor, cls=cls))
