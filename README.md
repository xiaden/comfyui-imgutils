# ImgUtils Nodes for ComfyUI

ComfyUI custom nodes wrapping [deepghs/imgutils](https://github.com/deepghs/imgutils) — a comprehensive toolbox for anime image analysis, tagging, detection, pose estimation, and segmentation.

All nodes use the **ComfyUI V2 `io.ComfyNode` API**. Requires ComfyUI ≥ 0.25.0.

## Nodes (34)

### Tagging & Tags (7)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils WD14 Tagger** | `imgutils/tagging` | `general_threshold` (0.35), `character_threshold` (0.85), `drop_overlap` | `tags`, `json` |
| **Imgutils DeepDanbooru Tagger** | `imgutils/tagging` | `general_threshold` (0.5), `character_threshold` (0.5), `drop_overlap` | `tags`, `json` |
| **Imgutils DeepGelbooru Tagger** | `imgutils/tagging` | `general_threshold` (0.3), `character_threshold` (0.3), `drop_overlap` | `tags`, `json` |
| **Imgutils MLDanbooru Tagger** | `imgutils/tagging` | `threshold` (0.7), `drop_overlap` — *truncated to top 50 tags* | `tags`, `json` |
| **Imgutils Camie Tagger** | `imgutils/tagging` | `mode` (Balanced, High Precision, High Recall, Micro Optimized, Macro Optimized), `drop_overlap` | `tags`, `json` |
| **Imgutils PixAI Tagger** | `imgutils/tagging` | `threshold` (0.4), `drop_overlap` — *truncated to top 50 tags* | `tags`, `json` |
| **Imgutils Tags** | `imgutils/tagging` | `mode`, `tags` — 9 ops: filter (blacklisted, basic character, overlap), sort (original, by score, shuffle), format (spaces↔underscores, text) | `tags` |

> **Note:** MLDanbooru and PixAI taggers return flat dicts (truncated to top 50 tags), unlike WD14/DeepDanbooru/DeepGelbooru/Camie which split output into Rating, General Tags, and Characters sections. The `json` output format reflects this difference.

### Judge (3)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Classify** | `imgutils/judge` | `mode` (Safe Check) — 11 ops: Safe Check, NSFW Prediction, Anime Rating, Anime DB Rating, Anime Teen, Anime Classify, Anime Real, Anime Portrait, Anime Furry, Anime Bangumi Character, Anime Style Age | `label`, `score`, `json` |
| **Imgutils Check** | `imgutils/judge` | `mode` (Is AI Created) — 5 ops: Is AI Created, Is Monochrome, Is Greyscale, Is Truncated, Anime Completeness | `label`, `boolean` (BOOL), `json` |
| **Imgutils Metric** | `imgutils/judge` | `mode` (Laplacian Score) — 2 ops: Laplacian Score (sharpness), Monochrome Score | `label`, `score`, `json` |

### OCR (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils OCR** | `imgutils/ocr` | `heat_threshold` (0.3), `box_threshold` (0.7) — PaddleOCR text extraction | `detections`, `json` |

### Detect (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Detect** | `imgutils/detect` | `mode` (Detect Faces) — 10 ops: Detect Faces, Detect Hands, Detect Heads, Detect Eyes, Detect Person, Detect Halfbody, Detect with NudeNet, Detect Censors, Detect Text with OCR, Detect with Booru YOLO; `confidence` (0.5) | `detections`, `json` |

### Edge (3)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Edge (Canny)** | `imgutils/edge` | `low_threshold` (100), `high_threshold` (200) | IMAGE |
| **Imgutils Edge (Lineart)** | `imgutils/edge` | `coarse` (false), `detect_resolution` (512) | IMAGE |
| **Imgutils Edge (Lineart Anime)** | `imgutils/edge` | `detect_resolution` (512) | IMAGE |

### Restore (3)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Restore (SCUNet)** | `imgutils/restore` | `mode` (GAN / PSNR), `tile_size` (128) | IMAGE |
| **Imgutils Restore (NAFNet)** | `imgutils/restore` | `mode` (REDS / GoPro / SIDD), `tile_size` (256) | IMAGE |
| **Imgutils Restore (Adversarial)** | `imgutils/restore` | — (no configurable knobs) | IMAGE |

### Transform (4)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Upscale (CDC)** | `imgutils/transform` | `tile_size` (512) — high quality anime upscaling | IMAGE |
| **Imgutils Censor** | `imgutils/transform` | `mode` (Pixelate / Blur / Color), `nipple_f`, `penis`, `pussy`, `confidence` (0.3) | IMAGE |
| **Imgutils Align** | `imgutils/transform` | `max_size` (1024) — resize longest side, preserve aspect ratio | IMAGE |
| **Imgutils Squeeze** | `imgutils/transform` | `threshold` (0.7), `median_filter` (5) — auto-crop to visible content | IMAGE |

### Compare (2)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Compare (CCIP)** | `imgutils/compare` | — (CCIP distance comparison, lower = more similar) | `label`, `distance` (FLOAT) |
| **Imgutils Compare (LPIPS)** | `imgutils/compare` | — (LPIPS perceptual similarity, lower = more similar) | `label`, `distance` (FLOAT) |

### Pose (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Pose** | `imgutils/pose` | `mode` (Full) — Body Only, Body with Face, Body with Hands, Full; `auto_detect` (true) — DWPose keypoints | IMAGE (`skeleton`), `json` |

### Segment (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Segment** | `imgutils/segment` | `scale` (1024) — isnetis character segmentation | MASK, IMAGE |

### Utility (8)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Bbox Unpack** | `imgutils/utility` | `bboxes` — parse OCR/Detect bbox output | `count` (INT), `labels`, `iterable` (JSON) |
| **Imgutils Bbox Crop** | `imgutils/utility` | `bboxes` — crop image to each bbox from Detect/OCR JSON | IMAGE (list — one per bbox) |
| **Imgutils Bbox Mask** | `imgutils/utility` | `bboxes` — create mask for each bbox from Detect/OCR JSON | MASK (list — one per bbox) |
| **Imgutils Label Contains** | `imgutils/utility` | `labels`, `search` — case-insensitive substring check | `boolean` (BOOL) |
| **Imgutils Boolean Logic** | `imgutils/utility` | `a` (BOOL), `b` (BOOL), `op` — AND, OR, XOR, NAND, NOR | `result` (BOOL) |
| **Imgutils Deduplicate Tags** | `imgutils/utility` | `tags` — merge multiple tag strings, deduplicate (supports multiple input wires) | `tags`, `count` (INT) |
| **Imgutils Score Threshold** | `imgutils/utility` | `score` (0.5), `threshold` (0.5) — boolean gate: score >= threshold | `boolean` (BOOL) |
| **Imgutils JSON Filter** | `imgutils/utility` | `json`, `threshold` (0.5) — filter scored JSON dict to entries above threshold | `json`, `tags`, `count` (INT) |

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
- `dghs-imgutils[gpu] >= 0.19.0` — the underlying analysis library with GPU-accelerated ONNX runtime
- `onnxruntime` — provided by ComfyUI's bundled runtime and pulled by `dghs-imgutils[gpu]` on install. In most cases no manual configuration is needed. If you encounter onnxruntime version conflicts, install the version matching your CUDA toolkit.

Models are downloaded automatically from HuggingFace Hub on first use and cached to `~/.cache/huggingface/hub/`. No manual model downloads needed.

## Structure

```
comfyui-imgutils/
├── __init__.py             # node registration table + ComfyExtension entrypoint
├── _shared/                # shared internals (not a node subpackage)
│   ├── bases.py            # _ImageToImage base class
│   ├── formatting.py       # string formatting and serialization helpers
│   └── tensor.py           # PIL ⇄ Comfy tensor conversion utilities
├── tagging/                # 7 tagger + tag-processing nodes
├── detect/                 # 2 detection + OCR nodes
├── pose/                   # 1 pose estimation node
├── segment/                # 1 character segmentation node
├── edge/                   # 3 edge detection nodes (Canny, Lineart, Anime)
├── restore/                # 3 restoration nodes (SCUNet, NAFNet, Adversarial)
├── compare/                # 2 comparison nodes (CCIP, LPIPS)
├── judge/                  # 3 classification/check/metric nodes
├── transform/              # 4 image transform nodes (CDC, Censor, Align, Squeeze)
└── utility/                # 7 utility nodes (Bbox, Label, Dedup, Score, JSON)
```

## License

MIT — see [LICENSE](./LICENSE).

`deepghs/imgutils` is also MIT-licensed.
