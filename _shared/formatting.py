"""
String formatting and serialization helpers for node outputs.
"""

import json
from typing import Any


def keypoints_to_json(keypoints_list: list[Any]) -> str:
    """Serialize OP18KeyPointSet objects to JSON keypoints."""
    result = []
    for kp in keypoints_list:
        person = {}
        for attr_name in ("body", "face", "left_hand", "right_hand", "left_foot", "right_foot"):
            arr = getattr(kp, attr_name, None)
            if arr is not None and len(arr) > 0:
                # Each row is (y, x, confidence) — convert to [x, y, confidence] for readability
                points = []
                for row in arr:
                    if len(row) >= 3:
                        points.append([float(row[1]), float(row[0]), float(row[2])])
                    elif len(row) >= 2:
                        points.append([float(row[1]), float(row[0]), 0.0])
                person[attr_name] = points
        result.append(person)

    return json.dumps(result, indent=2)


def join_tag_names(*sections: dict) -> str:
    """Join tag names from multiple dicts into a comma-separated string, sorted by confidence descending."""
    parts = []
    for d in sections:
        parts.extend(k for k, _v in sorted(d.items(), key=lambda x: x[1], reverse=True))
    return ", ".join(parts)


def label_display(raw: str) -> str:
    """Convert snake_case labels to Title Case for display."""
    return raw.replace("_", " ").title()
