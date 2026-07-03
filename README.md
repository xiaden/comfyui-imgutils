# ImgUtils Nodes for ComfyUI

ComfyUI custom nodes wrapping [deepghs/imgutils](https://github.com/deepghs/imgutils) — a comprehensive toolbox for anime image analysis, tagging, detection, pose estimation, and segmentation.

All nodes use the **ComfyUI V2 `io.ComfyNode` API**.

## Nodes (26)

### 🏷 Tagging (6)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils WD14 Tagger** | `imgutils/tagging` | `general_threshold`, `character_threshold`, `drop_overlap` |
| **Imgutils DeepDanbooru Tagger** | `imgutils/tagging` | `general_threshold`, `character_threshold`, `drop_overlap` |
| **Imgutils DeepGelbooru Tagger** | `imgutils/tagging` | `general_threshold`, `character_threshold`, `drop_overlap` |
| **Imgutils MLDanbooru Tagger** | `imgutils/tagging` | `threshold`, `drop_overlap` |
| **Imgutils Camie Tagger** | `imgutils/tagging` | `mode` (balanced/high_precision/…), `drop_overlap` |
| **Imgutils PixAI Tagger** | `imgutils/tagging` | `threshold` |
| **Imgutils Tags** | `imgutils/tagging` | Tag string processing — filter, sort, format |

### 🔎 Judge (3)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Classify** | `imgutils/judge` | 11 classification ops — safety, NSFW, rating, style, character |
| **Imgutils Check** | `imgutils/judge` | 5 boolean checks — AI-created, monochrome, greyscale, truncation, completeness |
| **Imgutils Metric** | `imgutils/judge` | 2 numeric metrics — sharpness (Laplacian), monochrome score |

### 📝 Describe (1)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils OCR** | `imgutils/describe` | `heat_threshold`, `box_threshold` — PaddleOCR text extraction |

### 🔍 Detect (1)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Detect** | `imgutils/detect` | `confidence` — faces, hands, heads, eyes, persons, half-bodies, text regions, nudenet, censors, Booru YOLO |

### ✏️ Edge (3)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Edge (Canny)** | `imgutils/edge` | `low_threshold`, `high_threshold` |
| **Imgutils Edge (Lineart)** | `imgutils/edge` | `coarse`, `detect_resolution` |
| **Imgutils Edge (Lineart Anime)** | `imgutils/edge` | `detect_resolution` |

### 🛠 Restore (3)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Restore (SCUNet)** | `imgutils/restore` | `model` (GAN/PSNR), `tile_size` |
| **Imgutils Restore (NAFNet)** | `imgutils/restore` | `model` (REDS/GoPro/SIDD), `tile_size` |
| **Imgutils Restore (Adversarial)** | `imgutils/restore` | Denoise adversarial noise — no ML model needed |

### 🎨 Transform (4)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Upscale (CDC)** | `imgutils/transform` | `tile_size` — high quality anime upscaling |
| **Imgutils Censor** | `imgutils/transform` | `method` (pixelate/blur/color), body-part toggles, `conf_threshold` |
| **Imgutils Align** | `imgutils/transform` | `max_size` — resize longest side, preserve aspect ratio |
| **Imgutils Squeeze** | `imgutils/transform` | `threshold`, `median_filter` — auto-crop to visible content |

### 📊 Compare (2)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Compare (CCIP)** | `imgutils/compare` | Character identity similarity + same-character check |
| **Imgutils Compare (LPIPS)** | `imgutils/compare` | Perceptual similarity distance |

### 🦴 Pose (1)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Pose** | `imgutils/pose` | `visualization` preset, `auto_detect` — DWPose keypoints |

### ✂️ Segment (1)
| Node | Category | Knobs |
|------|----------|-------|
| **Imgutils Segment** | `imgutils/segment` | `scale` — isnetis character segmentation (mask + RGBA) |

## Installation

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/xiaden/comfyui-imgutils.git
cd comfyui-imgutils
pip install -r requirements.txt
```

Or install via ComfyUI-Manager (once published to the Registry).

## Requirements

- Python >= 3.10
- `dghs-imgutils >= 0.19.0` — the underlying analysis library (installed via `requirements.txt`)
- `onnxruntime` — for ONNX model inference. ComfyUI already ships both `onnxruntime` (CPU) and `onnxruntime-gpu` (CUDA) in its venv. The `dghs-imgutils[gpu]` extra also pulls `onnxruntime-gpu` on install, so there is nothing to manually install or replace.

Models are downloaded automatically from HuggingFace Hub on first use and cached to `~/.cache/huggingface/hub/`. No manual model downloads needed.

## Structure

```
imgutils_nodes/
├── __init__.py           # NODE_CLASS_MAPPINGS + ComfyExtension entrypoint
├── node_*.py             # Root nodes (OCR, Detect, Pose, Segment, Tags, CDC, Censor, Align, Squeeze)
├── tagging/              # 6 tagger nodes — one per model
├── edge/                 # 3 edge detection nodes
├── restore/              # 3 restoration/denoising nodes
├── compare/              # 2 image comparison nodes
├── judge/                # 3 image analysis nodes
└── utils.py              # PIL ↔ ComfyUI tensor conversion
```

## License

MIT — see [LICENSE](./LICENSE).

`deepghs/imgutils` is also MIT-licensed.
