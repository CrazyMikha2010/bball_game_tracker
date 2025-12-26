# bball_game_tracker

Beautiful, modular tools for tracking basketball games using computer vision.

This repository provides scripts, models, and notebooks to detect rims, estimate player pose/keypoints, and draw court overlays — useful for analytics, coaching, and research.

## Highlights

- Rim & hoop detection using object-detection models (in `object_detection/`).
- Player keypoint / pose estimation and court overlay utilities (in `court_scheme/`).
- Notebooks and quick experiments to help you run demos and iterate on models (in `testing/` and `training_models/`).

## Table of contents

- [bball\_game\_tracker](#bball_game_tracker)
  - [Highlights](#highlights)
  - [Table of contents](#table-of-contents)
  - [Quick start](#quick-start)
  - [Project structure](#project-structure)
  - [Usage examples](#usage-examples)
  - [Development \& training](#development--training)
  - [Tips \& best practices](#tips--best-practices)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Quick start

1. Clone the repo and enter the project directory:

   git clone <repo-url>
   cd bball_game_tracker

2. (Recommended) Create a Python virtual environment and activate it:

   python3 -m venv .venv
   source .venv/bin/activate

3. Install common dependencies (example; pin versions in a `requirements.txt` for reproducibility):

   pip install -U pip
   pip install opencv-python numpy matplotlib torch torchvision pytorch-lightning mediapipe scikit-learn

Note: If this repo adds a `requirements.txt` later, replace the install line with `pip install -r requirements.txt`.

## Project structure

- `court_scheme/`
  - `court_drawer.py` — utilities to draw court overlays and annotate frames.
  - `keypoint_detector.py` — keypoint/pose estimation helper functions and wrappers.
- `object_detection/`
  - `pl_bball_rim_detector.py` — (PyTorch Lightning) rim/hoop detector model and training/inference logic.
- `testing/`
  - `pose_estimation.ipynb` — interactive notebook demonstrating pose estimation and visualizations.
- `training_models/`
  - training experiments and helper scripts.
- `README.md`, `LICENSE`, `process_journal.md`

## Usage examples

These are suggested quick actions to explore repository components. Exact CLI flags depend on scripts' implementations; check the top of each script for usage notes or ask me to add explicit CLI support.

- Run the pose estimation demo:
  - Open and run `testing/pose_estimation.ipynb` in Jupyter or JupyterLab.

- Try the court overlay utilities in a small script:
  - Import functions from `court_scheme/court_drawer.py` and feed a sample frame sequence (video or webcam).

- Run rim detection (inference):
  - Inspect `object_detection/pl_bball_rim_detector.py` for an `inference` or `predict` function. If missing, I can add a small example CLI for you.

If you'd like, I can add one-click commands (e.g., `scripts/run_demo.sh` or CLI flags like `--input`/`--output`) for the most common flows — tell me which script you use most.

## Development & training

- If you train or fine-tune models, keep experiments reproducible:
  - Create a `requirements.txt` and pin package versions.
  - Use deterministic seeds where possible.
  - Log experiments with lightweight tools (TensorBoard, WandB, or CSV logs).

- Typical steps to train a model:
  1. Prepare/annotate your dataset (images + bounding boxes or keypoints).
  2. Implement dataset loader and augmentations compatible with the model code in `object_detection/` or `training_models/`.
  3. Start training with the repo's training script or add a new one (PyTorch Lightning-friendly examples are in `object_detection/`).

## Tips & best practices

- Use smaller subsets of data and a low number of epochs for quick iteration.
- Validate on held-out videos to check robustness to camera angles and lighting.
- For live/tracking use-cases, prefer lightweight models and batch/frame-rate optimizations.

## Contributing

Contributions are welcome. A good workflow:

1. Fork the repo and create a branch for your change.
2. Keep changes small and focused (feature, bugfix, or documentation).
3. Open a pull request describing your change and add screenshots or short recordings when relevant.

If you'd like, I can add CONTRIBUTING.md with a PR template and a checklist for model training experiments.
