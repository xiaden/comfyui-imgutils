"""
ComfyUI IMAGE tensor <-> PIL.Image conversion utilities.
"""

import numpy as np
from PIL import Image


def comfy_to_pil(image_tensor) -> Image.Image:
    """Convert a ComfyUI IMAGE tensor to a PIL Image. Only the first image in the batch is processed."""
    img = image_tensor.numpy()[0].copy()
    img = (img * 255.0).clip(0, 255).astype(np.uint8)
    return Image.fromarray(img, mode="RGB")


def pil_to_comfy(pil_image: Image.Image) -> np.ndarray:
    """Convert a PIL Image to a ComfyUI IMAGE tensor."""
    if pil_image.mode not in ("RGB", "RGBA", "L", "1"):
        pil_image = pil_image.convert("RGB")

    if pil_image.mode in ("L", "1"):
        img = np.array(pil_image, dtype=np.float32) / 255.0
        img = img[:, :, np.newaxis]
        img = img[np.newaxis, ...]
    else:
        img = np.array(pil_image, dtype=np.float32) / 255.0
        img = img[np.newaxis, ...]

    return img
