"""
Shared internals for imgutils_nodes — registration helper and re-exports.

This package is prefixed with underscore to signal that it is not a
node subpackage.  Consumer code imports individual modules explicitly.
"""

import logging
import importlib

logger = logging.getLogger(__name__)


def register_nodes(
    package: str, nodes: list[tuple[str, str, str]]
) -> tuple[dict, dict]:
    """Import and register node classes from a subpackage."""
    class_mappings: dict[str, type] = {}
    display_mappings: dict[str, str] = {}

    for module_name, class_name, display_name in nodes:
        try:
            mod = importlib.import_module(f"{package}.{module_name}")
            class_mappings[class_name] = getattr(mod, class_name)
            display_mappings[class_name] = display_name
        except Exception:
            logger.warning(f"{class_name} unavailable.", exc_info=True)

    return class_mappings, display_mappings
