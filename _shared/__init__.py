"""Shared internals for imgutils_nodes.

This package is prefixed with underscore to signal that it is not a
node subpackage.  Consumer code imports individual modules explicitly.
"""

import logging

logger = logging.getLogger(__name__)
