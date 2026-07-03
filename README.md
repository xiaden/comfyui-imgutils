# ImgUtils Nodes for ComfyUI

ComfyUI custom nodes wrapping [deepghs/imgutils](https://github.com/deepghs/imgutils) — a comprehensive toolbox for anime image analysis, tagging, detection, pose estimation, and segmentation.

All nodes use the **ComfyUI V2 `io.ComfyNode` API**.

## Nodes (27)

### 🏷 Tagging & Tags (7)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils WD14 Tagger** | `imgutils/tagging` | `general_threshold` (0.35), `character_threshold` (0.85), `drop_overlap` | `tags`, `scores` |
| **Imgutils DeepDanbooru Tagger** | `imgutils/tagging` | `general_threshold` (0.5), `character_threshold` (0.5), `drop_overlap` | `tags`, `scores` |
| **Imgutils DeepGelbooru Tagger** | `imgutils/tagging` | `general_threshold` (0.3), `character_threshold` (0.3), `drop_overlap` | `tags`, `scores` |
| **Imgutils MLDanbooru Tagger** | `imgutils/tagging` | `threshold` (0.7), `drop_overlap` — *truncated to top 50 tags* | `tags`, `scores` |
| **Imgutils Camie Tagger** | `imgutils/tagging` | `mode` (balanced, high_precision, high_recall, micro_opt, macro_opt), `drop_overlap` | `tags`, `scores` |
| **Imgutils PixAI Tagger** | `imgutils/tagging` | `threshold` (0.4) — *truncated to top 50 tags* | `tags`, `scores` |
| **Imgutils Tags** | `imgutils/tagging` | `operation`, `tags` — 9 ops: filter (blacklisted, basic_character, overlap), sort (original, score, shuffle), format (spaces↔underscores, text) | `tags` |

### 🔎 Judge (3)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Classify** | `imgutils/judge` | `operation` (safe_check) — 11 ops: safe_check, nsfw_pred, anime_rating, anime_dbrating, anime_teen, anime_classify, anime_real, anime_portrait, anime_furry, anime_bangumi_char, anime_style_age | `label`, `score`, `full_response` |
| **Imgutils Check** | `imgutils/judge` | `operation` (is_ai_created) — 5 ops: is_ai_created, is_monochrome, is_greyscale, is_truncated, anime_completeness | `result`, `detail` |
| **Imgutils Metric** | `imgutils/judge` | `operation` (laplacian_score) — 2 ops: laplacian_score (sharpness), monochrome_score | `label`, `score` |

### 📝 Describe (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils OCR** | `imgutils/describe` | `heat_threshold` (0.3), `box_threshold` (0.7) — PaddleOCR text extraction | `text`, `scores`, `bboxes` |

### 🔍 Detect (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Detect** | `imgutils/detect` | `operation` (detect_faces) — 10 ops: detect_faces, detect_hands, detect_heads, detect_eyes, detect_person, detect_halfbody, detect_with_nudenet, detect_censors, detect_text_with_ocr, detect_with_booru_yolo; `confidence` (0.5) | `detections`, `boxes`, `bboxes` |

### ✏️ Edge (3)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Edge (Canny)** | `imgutils/edge` | `low_threshold` (100), `high_threshold` (200) | IMAGE |
| **Imgutils Edge (Lineart)** | `imgutils/edge` | `coarse` (false), `detect_resolution` (512) | IMAGE |
| **Imgutils Edge (Lineart Anime)** | `imgutils/edge` | `detect_resolution` (512) | IMAGE |

### 🛠 Restore (3)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Restore (SCUNet)** | `imgutils/restore` | `model` (GAN / PSNR), `tile_size` (128) | IMAGE |
| **Imgutils Restore (NAFNet)** | `imgutils/restore` | `model` (REDS / GoPro / SIDD), `tile_size` (256) | IMAGE |
| **Imgutils Restore (Adversarial)** | `imgutils/restore` | — (no configurable knobs) | IMAGE |

### 🎨 Transform (4)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Upscale (CDC)** | `imgutils/transform` | `tile_size` (512) — high quality anime upscaling | IMAGE |
| **Imgutils Censor** | `imgutils/transform` | `method` (pixelate / blur / color), `nipple_f`, `penis`, `pussy`, `conf_threshold` (0.3) | IMAGE |
| **Imgutils Align** | `imgutils/transform` | `max_size` (1024) — resize longest side, preserve aspect ratio | IMAGE |
| **Imgutils Squeeze** | `imgutils/transform` | `threshold` (0.7), `median_filter` (5) — auto-crop to visible content | IMAGE |

### 📊 Compare (2)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Compare (CCIP)** | `imgutils/compare` | `operation` (ccip_difference) — ccip_difference (similarity distance) or ccip_same (same-character boolean) | `text` |
| **Imgutils Compare (LPIPS)** | `imgutils/compare` | — (no configurable knobs) | `text` |

### 🦴 Pose (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Pose** | `imgutils/pose` | `visualization` (full) — body_only, body_with_face, body_with_hands, full; `auto_detect` (true) — DWPose keypoints | IMAGE, `keypoints_json` |

### ✂️ Segment (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Segment** | `imgutils/segment` | `scale` (1024) — isnetis character segmentation | MASK, IMAGE (RGBA) |

### 🔧 Utility (1)
| Node | Category | Knobs | Outputs |
|------|----------|-------|---------|
| **Imgutils Bbox Unpack** | `imgutils/bbox` | `bbox_string` — parse OCR/Detect bbox output | `count` (INT), `labels`, `iterable` (JSON) |

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
- `onnxruntime` — provided by ComfyUI (ships both CPU and GPU variants in its venv) and pulled by `dghs-imgutils[gpu]` on install. Nothing to manually configure.

Models are downloaded automatically from HuggingFace Hub on first use and cached to `~/.cache/huggingface/hub/`. No manual model downloads needed.

## Structure

```
comfyui-imgutils/
├── __init__.py           # NODE_CLASS_MAPPINGS + ComfyExtension entrypoint
├── node_*.py             # Root nodes (OCR, Detect, Pose, Segment, Tags, CDC, Censor, Align, Squeeze, Bbox)
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
