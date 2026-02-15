# Adaptive Multi-Metric Framework for Intelligent Image Enhancement

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

A comprehensive, modular Python framework for **automated image enhancement** using classical computer vision techniques. The system intelligently selects optimal enhancement methods by evaluating multiple objective quality metrics and computing adaptive composite scores.

## 🎯 Project Overview

This framework automates the process of enhancing low-quality images by:

1. **Applying multiple enhancement techniques** to each image
2. **Computing objective quality metrics** for each enhanced result
3. **Normalizing metrics** to a common scale
4. **Computing weighted composite scores** with configurable importance weights
5. **Automatically selecting** the best enhancement method
6. **Generating visualizations** and comprehensive reports

### Key Features

✨ **Four Enhancement Techniques**
- Histogram Equalization - Global contrast improvement
- CLAHE - Adaptive local contrast with noise limitation
- Gamma Correction - Brightness adjustment via power-law transformation
- Bilateral Filtering - Edge-preserving smoothing and noise reduction

📊 **Four Quality Metrics**
- **Entropy** - Information content and detail richness (Shannon entropy)
- **PSNR** - Peak Signal-to-Noise Ratio (fidelity measure)
- **SSIM** - Structural Similarity Index (perceptual similarity)
- **Contrast** - Image contrast via standard deviation of intensities

🔧 **Intelligent Scoring System**
- Min-Max normalization of metrics to [0, 1] range
- Weighted composite score: `Score = w₁M₁ + w₂M₂ + w₃M₃ + w₄M₄`
- Configurable weights for fine-tuning importance of each metric
- **Adaptive weight selection** based on image characteristics

🎨 **Comprehensive Visualizations**
- Side-by-side comparison of all enhancement methods
- Bar charts comparing metrics across methods
- Metric distribution analysis
- Publication-ready PNG outputs

📋 **Detailed Reporting**
- CSV export of all metrics and scores
- Summary statistics across processed images
- Best method ranking and win counts
- Reproducible research documentation

## 📁 Project Structure

```
adaptive_image_enhancement/
│
├── data/
│   ├── input_images/          # Place your images here
│   ├── output_images/         # Enhanced images saved here
│   └── test_dataset/          # Sample test images (optional)
│
├── src/
│   ├── enhancement/           # Enhancement technique modules
│   │   ├── histogram_equalization.py
│   │   ├── clahe.py
│   │   ├── gamma_correction.py
│   │   └── bilateral_filter.py
│   │
│   ├── metrics/              # Quality metrics modules
│   │   ├── entropy.py        # Shannon entropy calculation
│   │   ├── psnr.py           # PSNR calculation
│   │   ├── ssim.py           # SSIM calculation
│   │   └── contrast.py       # Contrast metric
│   │
│   ├── scoring/              # Scoring and selection modules
│   │   ├── normalization.py  # Min-Max normalization
│   │   └── composite_score.py # Composite scoring & adaptive weights
│   │
│   └── utils/                # Utility functions
│       ├── image_loader.py   # Image I/O
│       ├── visualization.py  # Plot generation
│       └── table_export.py   # CSV export
│
├── notebooks/
│   └── experiments.ipynb      # Interactive experiments & analysis
│
├── results/
│   ├── graphs/               # Metric comparison plots
│   ├── comparison_tables/    # CSV result files
│   └── best_outputs/         # Best enhanced images
│
├── main.py                    # Main execution script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone/Navigate to the project directory**
```bash
cd adaptive_image_enhancement
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

#### Basic Usage

Process all images in the `data/input_images/` directory:

```bash
python main.py data/input_images
```

#### Advanced Usage

**With custom output directories:**
```bash
python main.py data/input_images --output results/enhanced --results results/analysis
```

**With adaptive weight selection:**
```bash
python main.py data/input_images --adaptive
```

**Get help:**
```bash
python main.py --help
```

### Output Structure

After running, the following outputs are generated:

```
data/output_images/           # All enhanced images for each method
results/
├── graphs/                   # PNG visualizations
│   ├── image1_comparison.png
│   └── image1_metrics.png
├── comparison_tables/        # CSV analysis
│   ├── detailed_metrics.csv
│   ├── summary.csv
│   └── best_methods_summary.csv
└── best_outputs/             # Best enhancement for each image
```

## 📊 Enhancement Techniques in Detail

### 1. Histogram Equalization
Redistributes pixel intensities uniformly across the intensity range.

**Use Case**: Low-contrast images, images with narrow histograms

```python
from src.enhancement import apply_histogram_equalization
enhanced = apply_histogram_equalization(image)
```

### 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
Local histogram equalization with contrast limiting to prevent noise amplification.

**Use Case**: Images with noise, uneven illumination

```python
from src.enhancement import apply_clahe
enhanced = apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8))
```

### 3. Gamma Correction
Non-linear power-law transformation for brightness adjustment.

**Use Case**: Dark images (γ < 1), bright images (γ > 1)

```python
from src.enhancement import apply_gamma_correction
enhanced = apply_gamma_correction(image, gamma=1.2)
```

### 4. Bilateral Filtering
Edge-preserving smoothing that reduces noise while preserving boundaries.

**Use Case**: Noisy images, images requiring denoising

```python
from src.enhancement import apply_bilateral_filter
enhanced = apply_bilateral_filter(image, diameter=9, sigma_color=75, sigma_space=75)
```

## 📈 Quality Metrics Explained

### Entropy (Shannon Entropy)
Measures information content and detail richness.

**Higher is better**: More information = clearer image

**Range**: 0-8 bits (typical for 8-bit images)

**Formula**: H = -Σ(p_i * log₂(p_i))

### PSNR (Peak Signal-to-Noise Ratio)
Ratio of maximum possible power to noise power.

**Higher is better**: Better fidelity to original

**Range**: Typically 20-50 dB

**Interpretation**:
- < 20 dB: Poor quality
- 20-30 dB: Fair quality
- > 40 dB: Excellent quality

**Formula**: PSNR = 10·log₁₀(MAX²/MSE)

### SSIM (Structural Similarity Index)
Perceptual similarity between images, better correlates with human vision.

**Higher is better**: Greater structural similarity

**Range**: -1 to 1 (typically 0 to 1)

**Interpretation**:
- 1.0: Identical images
- > 0.9: Very similar
- > 0.8: Similar
- < 0.5: Dissimilar

### Contrast (Standard Deviation)
Spread of pixel intensities indicating visual distinction between regions.

**Higher is better**: Greater visual separation

**Range**: 0-255

**Formula**: σ = √(E[(X - μ)²])

## 🎛️ Scoring System

### Min-Max Normalization

Each metric is normalized to [0, 1] range:

```
X_normalized = (X - X_min) / (X_max - X_min)
```

This allows fair comparison between different metric scales.

### Composite Score Calculation

The final score is a weighted combination of normalized metrics:

```
Score = w_entropy × Entropy + w_psnr × PSNR + w_ssim × SSIM + w_contrast × Contrast
```

where weights sum to 1.0.

**Default equal weights**: 0.25 each

### Adaptive Weight Selection

The framework can automatically adjust weights based on image characteristics:

| Image Condition | Entropy | PSNR | SSIM | Contrast |
|---|---|---|---|---|
| **Dark Image** | ↑ 0.35 | 0.20 | 0.15 | ↑ 0.30 |
| **Noisy Image** | 0.25 | 0.20 | ↑ 0.35 | 0.20 |
| **Low Contrast** | ↑ 0.30 | 0.20 | 0.15 | ↑ 0.35 |
| **Normal** | 0.25 | 0.25 | 0.25 | 0.25 |

Enable adaptive weights:
```bash
python main.py data/input_images --adaptive
```

## 🔬 Using the Framework Programmatically

### Quick Example

```python
from pathlib import Path
import sys
sys.path.insert(0, 'src')

from enhancement import apply_clahe, apply_gamma_correction
from metrics import calculate_entropy, calculate_ssim, calculate_contrast
from scoring import compute_composite_score
import cv2

# Load image
image = cv2.imread('image.jpg')

# Apply enhancements
enhanced_clahe = apply_clahe(image)
enhanced_gamma = apply_gamma_correction(image)

# Compute metrics
metrics = {
    'CLAHE': {
        'entropy': calculate_entropy(enhanced_clahe),
        'contrast': calculate_contrast(enhanced_clahe),
        'ssim': calculate_ssim(enhanced_clahe)
    },
    'Gamma': {
        'entropy': calculate_entropy(enhanced_gamma),
        'contrast': calculate_contrast(enhanced_gamma),
        'ssim': calculate_ssim(enhanced_gamma)
    }
}

# Score and select best
result = compute_composite_score(metrics)
print(f"Best method: {result['best_method']}")
print(f"Score: {result['best_score']:.4f}")
```

### Custom Weight Configuration

```python
custom_weights = {
    'entropy': 0.4,      # Emphasize clarity
    'psnr': 0.1,
    'ssim': 0.3,         # Emphasize structure
    'contrast': 0.2
}

result = compute_composite_score(metrics, weights=custom_weights)
```

### Adaptive Weights

```python
from scoring import compute_adaptive_weights

# Automatically determine weights based on image
adaptive_w = compute_adaptive_weights(image)
result = compute_composite_score(metrics, weights=adaptive_w)
```

## 📓 Jupyter Notebook Experiments

Interactive experiments and demonstrations are available in `notebooks/experiments.ipynb`:

1. **Setup and Imports** - Initialize the framework
2. **Create Test Images** - Generate synthetic low-quality images
3. **Apply Enhancements** - Demonstrate all techniques
4. **Visualize Results** - Side-by-side comparisons
5. **Compute Metrics** - Evaluate all methods
6. **Test Scoring** - Compare different weight configurations
7. **Adaptive Weights** - Test automatic weight selection
8. **Sensitivity Analysis** - Analyze weight sensitivity
9. **Batch Processing** - Process multiple images

Run the notebook:
```bash
jupyter notebook notebooks/experiments.ipynb
```

## 📋 Output Files

### CSV Reports

**detailed_metrics.csv**
- Per-image, per-method detailed metrics
- Both raw and normalized values
- Best method indicator

**summary.csv**
- One row per image
- Best method and score for each image
- Average metrics across all methods

**best_methods_summary.csv**
- Method rankings across all images
- Win counts and percentages

### PNG Visualizations

**image_name_comparison.png**
- Original image vs. all enhanced versions
- Side-by-side visual comparison

**image_name_metrics.png**
- Composite score bar chart
- Individual metric comparison charts

## 🔍 Understanding the Results

### High Entropy
Indicates a clear, detailed image with good information content.

→ Good for image clarity assessment

### High PSNR
Indicates high fidelity to the original image.

→ Good when preserving fidelity is important

### High SSIM
Indicates structural similarities are preserved.

→ Good for perceptually pleasing results

### High Contrast
Indicates good separation between light and dark regions.

→ Good for visibility and distinction

## ⚙️ Configuration & Customization

### Modify Enhancement Parameters

Edit enhancement functions in `src/enhancement/`:

```python
# Example: Adjust CLAHE parameters
enhanced = apply_clahe(image, clip_limit=3.0, tile_grid_size=(16, 16))
```

### Custom Metrics

Add new metrics by creating a module in `src/metrics/`:

```python
# src/metrics/custom_metric.py
def calculate_custom_metric(image):
    """Your custom metric implementation"""
    # Your code here
    return metric_value
```

### Custom Enhancement Methods

Add enhancement techniques in `src/enhancement/`, then update `main.py`:

```python
self.enhancement_methods['new_method'] = apply_new_method
```

## 📊 Performance Considerations

| Aspect | Performance |
|--------|-------------|
| **Speed** | Fast (seconds per image) |
| **Memory** | Moderate (< 1GB typical) |
| **Scalability** | Processes multiple images efficiently |
| **GPU Support** | Not required (CPU only) |

**Processing Time Estimates** (for 256×256 image):
- Histogram Equalization: ~5ms
- CLAHE: ~50ms
- Gamma Correction: ~3ms
- Bilateral Filter: ~100ms
- All Metrics: ~30ms
- **Total per image**: ~200ms

## 🔬 Research Applications

This framework is suitable for:

- **Image Enhancement Evaluation** - Compare methods scientifically
- **Benchmark Studies** - Test enhancement techniques systematically
- **Quality Assessment** - Automated image quality evaluation
- **Image Preprocessing** - Prepare images for downstream tasks
- **Algorithm Development** - Test new enhancement methods
- **Publication Support** - Generate reproducible results with visualizations

## 📖 Citation

If you use this framework in research, please cite:

```bibtex
@software{adaptive_image_enhancement,
  title={Adaptive Multi-Metric Framework for Intelligent Image Enhancement},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/adaptive_image_enhancement}
}
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### ImportError: No module named 'cv2'

Install required packages:
```bash
pip install -r requirements.txt
```

### No images found error

Ensure images are in the correct directory:
```bash
ls data/input_images/
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

### Memory Issues

For large images, reduce bilateral filter diameter or process images in batches.

## 📞 Support

For issues, questions, or suggestions, please:
- Create an issue on GitHub
- Check existing documentation
- Review the experiments notebook for examples

## 🎓 Educational Value

This framework demonstrates:

- Professional Python package structure
- NumPy/OpenCV image processing
- Signal processing concepts (FFT, convolution)
- Statistical analysis and normalization
- Scientific visualization with matplotlib
- CSV data export and analysis
- Reproducible research practices
- Documentation best practices

## 🚀 Future Enhancements

Potential improvements:

- [ ] Deep learning-based enhancement methods
- [ ] More sophisticated adaptive weight selection
- [ ] GPU acceleration support
- [ ] Batch processing with progress bar
- [ ] Web interface for interactive enhancement
- [ ] Real-time image enhancement preview
- [ ] Machine learning for optimal weight prediction
- [ ] Support for video enhancement

---

**Made with ❤️ for image enhancement research**

Last Updated: February 2024

Documentation Version: 1.0
