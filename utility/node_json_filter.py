"""Filter scored JSON dict/tagger output to entries above a confidence threshold."""

import json as _json
from comfy_api.latest import io


class ImgUtilsJSONFilter(io.ComfyNode):
    """Filter scored JSON (from taggers/classifiers) to entries above a threshold."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImgUtilsJSONFilter",
            display_name="Imgutils JSON Filter",
            category="imgutils/utility",
            description=(
                "Filter a scored JSON dict (from Tagger or Classify json output) "
                "to only entries with score >= threshold."
            ),
            search_aliases=["json", "filter", "threshold", "tags", "scores"],
            inputs=[
                io.String.Input("json", tooltip="JSON string dict of {key: score} to filter."),
                io.Float.Input("threshold", default=0.5, min=0.0, max=1.0, step=0.01, tooltip="Minimum score to keep."),
            ],
            outputs=[
                io.String.Output(display_name="json"),
                io.String.Output(display_name="tags"),
                io.Int.Output(display_name="count"),
            ],
        )

    @classmethod
    def execute(cls, json, threshold) -> io.NodeOutput:
        t = threshold

        try:
            data = _json.loads(json) if isinstance(json, str) else {}
        except _json.JSONDecodeError:
            data = {}

        # Flatten nested dicts (e.g., {"rating": {...}, "general": {...}, "character": {...}})
        if data and all(isinstance(v, dict) for v in data.values()):
            flat: dict[str, float] = {}
            for k, v in data.items():
                if isinstance(v, dict):
                    flat.update(v)
            data = flat

        filtered = {k: v for k, v in data.items() if isinstance(v, (int, float)) and float(v) >= t}
        sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
        filtered_json = _json.dumps(dict(sorted_items), ensure_ascii=False)
        tags = ", ".join(k for k, _ in sorted_items)
        return io.NodeOutput(filtered_json, tags, len(sorted_items))
