"""imgutils_nodes judge sub-package — classification, boolean checks, and quality metrics."""

from .node_classify import ImgUtilsClassify
from .node_check import ImgUtilsCheck
from .node_metric import ImgUtilsMetric

NODE_CLASSES = [ImgUtilsClassify, ImgUtilsCheck, ImgUtilsMetric]
