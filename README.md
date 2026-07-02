# ImgUtils Nodes for ComfyUI

ComfyUI custom nodes wrapping [deepghs/imgutils](https://github.com/deepghs/imgutils) — a comprehensive toolbox for anime image analysis, tagging, detection, pose estimation, and segmentation.

## Nodes

| Node | Category | Description |
|---|---|---|
| **Imgutils Judge** | `imgutils/validate` | Classify and validate images — safety, NSFW, ratings, style, AI detection, completeness, aesthetic scoring |
| **Imgutils Describe** | `imgutils/describe` | Tag images with WD14/DeepDanbooru/MLDanbooru/Camie/PixAI, detect faces/hands/eyes/persons, run OCR |
| **Imgutils Transform** | `imgutils/transform` | Edge detection (Canny/Lineart), image restoration, upscaling, NSFW censoring, alignment, transparency squeeze |
| **Imgutils Compare** | `imgutils/compare` | Compare two images with CCIP character similarity or LPIPS perceptual distance |
| **Imgutils Pose** | `imgutils/pose` | Detect human keypoints with DWPose and render visualization |
| **Imgutils Segment** | `imgutils/segment` | Segment anime character from background using isnetis |
| **Imgutils Tags** | `imgutils/tagging` | Process tag strings — filter, sort, format, convert between underscore/space styles |

## Installation

```bash
cd ComfyUI/custom_nodes/
git clone <repo-url> imgutils_nodes
cd imgutils_nodes
pip install -r requirements.txt
```

## Requirements

- Python >= 3.10
- `dghs-imgutils >= 0.19.0`

## License

MIT
