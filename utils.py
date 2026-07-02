"""
Shared utilities for imgutils ComfyUI custom nodes.

Handles ComfyUI IMAGE tensor <-> PIL.Image conversion and result formatting.
"""

from __future__ import annotations

import json
import numpy as np
from PIL import Image
from typing import Any


def comfy_to_pil(image_tensor: np.ndarray) -> Image.Image:
    """
    Convert a ComfyUI IMAGE tensor to a PIL Image.

    ComfyUI IMAGE tensors are float32 with shape (B, H, W, C) in RGB order,
    where values are in [0.0, 1.0].

    Note:
        Only the **first image** in the batch is processed (``image_tensor[0]``).
        If you need to process a batch of images, iterate over the batch dimension
        before calling this function.

    Args:
        image_tensor: numpy array of shape (B, H, W, C), float32, RGB, [0,1]

    Returns:
        PIL.Image in RGB mode (from first image in batch)
    """
    # Take first image in batch
    img = image_tensor[0].copy()
    # float32 [0,1] -> uint8 [0,255]
    img = (img * 255.0).clip(0, 255).astype(np.uint8)
    return Image.fromarray(img, mode="RGB")


def pil_to_comfy(pil_image: Image.Image) -> np.ndarray:
    """
    Convert a PIL Image to a ComfyUI IMAGE tensor.

    Args:
        pil_image: PIL Image (any mode)

    Returns:
        numpy array of shape (1, H, W, C), float32, RGB (or RGBA for 4-channel), [0,1]
    """
    if pil_image.mode not in ("RGB", "RGBA", "L", "1"):
        pil_image = pil_image.convert("RGB")

    if pil_image.mode == "L":
        # Grayscale -> (H, W, 1) -> (1, H, W, 1)
        img = np.array(pil_image, dtype=np.float32) / 255.0
        img = img[:, :, np.newaxis]  # (H, W, 1)
        img = img[np.newaxis, ...]   # (1, H, W, 1)
    elif pil_image.mode == "1":
        img = np.array(pil_image, dtype=np.float32)
        img = img[:, :, np.newaxis]
        img = img[np.newaxis, ...]
    else:
        # RGB or RGBA
        img = np.array(pil_image, dtype=np.float32) / 255.0
        img = img[np.newaxis, ...]  # (1, H, W, C)

    return img


def keypoints_to_json(keypoints_list: list) -> str:
    """
    Serialize a list of OP18KeyPointSet objects to a JSON string.

    Each keypoint set has body, face, left_hand, right_hand, left_foot, right_foot
    properties that are numpy arrays. We convert each to a list of [x, y, confidence].

    Args:
        keypoints_list: list of OP18KeyPointSet objects from dwpose_estimate()

    Returns:
        JSON string with keypoints for all detected persons
    """
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
