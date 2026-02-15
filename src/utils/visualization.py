"""
Visualization Utility
Creates comparison visualizations and metric plots.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path


def visualize_comparison(original_image, enhanced_images, image_name, output_dir):
    """
    Create side-by-side comparison of original and enhanced images.
    
    Displays original image alongside all enhancement methods for visual
    comparison. Saves the figure to output directory.
    
    Parameters
    ----------
    original_image : np.ndarray
        Original input image (BGR format)
    enhanced_images : dict
        Dictionary of enhanced images:
        {
            'method_name': np.ndarray (BGR format),
            ...
        }
    image_name : str
        Name of the image (for title and filename)
    output_dir : str or Path
        Directory to save the comparison figure
        
    Returns
    -------
    str
        Path to saved figure
        
    Notes
    -----
    - Automatically converts BGR to RGB for matplotlib display
    - Creates subplot grid with original + all enhanced images
    - Saves high-quality PNG figure
    """
    from cv2 import cvtColor, COLOR_BGR2RGB
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Number of images: 1 original + all enhanced methods
    n_methods = len(enhanced_images)
    n_cols = min(3, n_methods + 1)  # Max 3 columns
    n_rows = (n_methods + 1 + n_cols - 1) // n_cols  # Round up division
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    
    # Flatten axes for easier indexing
    if n_rows * n_cols == 1:
        axes = [axes]
    elif n_rows == 1 or n_cols == 1:
        axes = axes.flatten()
    else:
        axes = axes.flatten()
    
    # Display original image
    original_rgb = cvtColor(original_image, COLOR_BGR2RGB)
    axes[0].imshow(original_rgb)
    axes[0].set_title('Original', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    # Display enhanced images
    for idx, (method_name, enhanced_img) in enumerate(enhanced_images.items(), 1):
        enhanced_rgb = cvtColor(enhanced_img, COLOR_BGR2RGB)
        axes[idx].imshow(enhanced_rgb)
        axes[idx].set_title(f'Enhanced: {method_name}', fontsize=12, fontweight='bold')
        axes[idx].axis('off')
    
    # Hide unused subplots
    for idx in range(len(enhanced_images) + 1, len(axes)):
        axes[idx].axis('off')
    
    plt.suptitle(f'Image Enhancement Comparison: {image_name}', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    # Save figure
    output_file = output_path / f"{image_name}_comparison.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved comparison: {output_file}")
    plt.close()
    
    return str(output_file)


def plot_metrics(metrics_scores, image_name, output_dir, normalized_metrics=None):
    """
    Create bar plots comparing metrics across enhancement methods.
    
    Generates two plots: one for normalized metrics and one for raw scores.
    
    Parameters
    ----------
    metrics_scores : dict
        Dictionary of scores:
        {
            'method_name': float (composite score),
            ...
        }
    image_name : str
        Name of the image (for title and filename)
    output_dir : str or Path
        Directory to save the comparison figure
    normalized_metrics : dict, optional
        Normalized metrics for detailed visualization:
        {
            'method_name': {
                'entropy': float,
                'psnr': float,
                'ssim': float,
                'contrast': float
            },
            ...
        }
        
    Returns
    -------
    str
        Path to saved figure
        
    Notes
    -----
    - Creates bar charts with color-coded methods
    - Highlights best method in green
    - Saves high-quality PNG figure
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Prepare data
    methods = list(metrics_scores.keys())
    scores = list(metrics_scores.values())
    
    # Find best method
    best_method = max(metrics_scores.items(), key=lambda x: x[1])[0]
    colors = ['green' if m == best_method else 'steelblue' for m in methods]
    
    # Create figure
    if normalized_metrics:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    
    # Plot 1: Composite scores
    ax1.bar(methods, scores, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Enhancement Method', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Composite Score', fontsize=12, fontweight='bold')
    ax1.set_title(f'Composite Scores - {image_name}', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, 1.0)
    ax1.grid(axis='y', alpha=0.3)
    for i, (method, score) in enumerate(zip(methods, scores)):
        ax1.text(i, score + 0.02, f'{score:.3f}', ha='center', fontweight='bold')
    
    # Plot 2: Individual metrics (if provided)
    if normalized_metrics:
        metric_names = list(next(iter(normalized_metrics.values())).keys())
        x = np.arange(len(methods))
        width = 0.2
        
        for idx, metric in enumerate(metric_names):
            values = [normalized_metrics[method][metric] for method in methods]
            ax2.bar(x + idx*width, values, width, label=metric.capitalize(),
                   edgecolor='black', linewidth=0.5)
        
        ax2.set_xlabel('Enhancement Method', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Normalized Metric Value', fontsize=12, fontweight='bold')
        ax2.set_title(f'Individual Metrics - {image_name}', fontsize=13, fontweight='bold')
        ax2.set_xticks(x + width * 1.5)
        ax2.set_xticklabels(methods)
        ax2.legend(loc='upper right')
        ax2.set_ylim(0, 1.1)
        ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = output_path / f"{image_name}_metrics.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved metrics plot: {output_file}")
    plt.close()
    
    return str(output_file)
