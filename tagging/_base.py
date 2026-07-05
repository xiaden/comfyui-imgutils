"""Shared base classes for tagger nodes."""

import json

from comfy_api.latest import io

from .._shared.tensor import comfy_to_pil
from .._shared.formatting import join_tag_names


class _SectionedTagger(io.ComfyNode):
    """Base for taggers that return rating / general / character sections.

    Subclasses define their own ``define_schema`` and ``execute``,
    calling ``_run`` with the appropriate tagger function and kwargs.
    """

    @staticmethod
    def _run(image, tagger_func, **kwargs) -> io.NodeOutput:
        """Execute a sectioned tagger: PIL convert, tag, format output."""
        pil_image = comfy_to_pil(image)
        rating, general, character = tagger_func(pil_image, **kwargs)
        tag_names = join_tag_names(rating, general, character)
        json_str = json.dumps(
            {"rating": rating, "general": general, "character": character},
            ensure_ascii=False,
        )
        return io.NodeOutput(tag_names, json_str)
