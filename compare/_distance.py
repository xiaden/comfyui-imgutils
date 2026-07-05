"""Distance-to-label mapping for comparison nodes."""


def _distance_label(distance: float, thresholds: list[tuple[float, str]]) -> str:
    """Map a distance to the first matching threshold label."""
    for threshold, label in thresholds:
        if distance <= threshold:
            return label
    return thresholds[-1][1]
