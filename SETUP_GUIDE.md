# Quick Setup Guide

## Issue Fixed ✅

**Problem**: `ModuleNotFoundError: No module named 'sklearn'`

**Solution**: Removed unused import from `src/metrics/ssim.py`
- The file was importing `cosine_similarity` from sklearn but never using it
- Removed the unnecessary import: `from sklearn.metrics._pairwise import cosine_similarity`
- The SSIM calculation already uses `scikit-image` which is properly listed in requirements

## Installation Instructions

Follow these steps to get the project running:

### Step 1: Install Dependencies

Run this command in the project directory:

```bash
pip install -r requirements.txt
```

Or install packages individually if you prefer:

```bash
pip install numpy opencv-python scikit-image matplotlib pandas jupyter ipython
```

### Step 2: Verify Installation

Test that all packages are installed:

```bash
python -c "import cv2; import skimage; import matplotlib; import pandas; import numpy; print('✓ All dependencies installed!')"
```

### Step 3: Run the Framework

**Basic usage:**
```bash
python main.py data/input_images
```

**With adaptive weights:**
```bash
python main.py data/input_images --adaptive
```

**View help:**
```bash
python main.py --help
```

## What Was Fixed

The `src/metrics/ssim.py` file had an unnecessary import that was causing the error:

```python
# REMOVED (not used in the code):
from sklearn.metrics._pairwise import cosine_similarity

# KEPT (these are the actual dependencies used):
from skimage.color import rgb2gray
from skimage.metrics import structural_similarity as ski_ssim
```

This fix eliminates sklearn as a dependency requirement, keeping the requirements list clean and minimal.

## Troubleshooting

If you encounter slow pip downloads, you can try:

```bash
# Use a different PyPI mirror
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
```

Or with the standard PyPI (may be slower):

```bash
pip install --no-cache-dir -r requirements.txt
```

Once dependencies are installed, the framework will run without any import errors!
