"""
Composite Score Calculation
Combines multiple metrics into a single quality score using weighted averaging.
"""

import numpy as np
from .normalization import normalize_metrics


def compute_composite_score(metrics_dict, weights=None, adaptive_weights=None):
    """
    Compute weighted composite score from normalized metrics.
    
    Combines multiple quality metrics into a single score using weighted
    averaging. Weights control the relative importance of each metric.
    
    Formula:
        Score = w1*M1 + w2*M2 + w3*M3 + w4*M4
    where Mi are normalized metrics [0,1] and wi are weights (sum=1).
    
    Parameters
    ----------
    metrics_dict : dict
        Dictionary with structure:
        {
            'method_name': {
                'entropy': float,
                'psnr': float,
                'ssim': float,
                'contrast': float
            },
            ...
        }
    weights : dict, optional
        Custom weights for each metric. Should sum to 1.0.
        Default: {'entropy': 0.25, 'psnr': 0.25, 'ssim': 0.25, 'contrast': 0.25}
        Example: {'entropy': 0.3, 'psnr': 0.2, 'ssim': 0.3, 'contrast': 0.2}
    adaptive_weights : dict, optional
        Image-dependent weights for adaptive scoring.
        Overrides fixed weights if provided.
        Contains same keys as weights.
        
    Returns
    -------
    dict
        Dictionary with results:
        {
            'best_method': str,           # Name of best enhancement method
            'best_score': float,          # Score of best method [0, 1]
            'all_scores': dict,           # Scores of all methods
            'normalized_metrics': dict,   # All normalized metric values
            'weights_used': dict          # Weights applied in calculation
        }
        
    Notes
    -----
    - All returned scores are normalized to [0, 1]
    - Best method has highest composite score
    - Weights should sum to 1.0 for interpretability
    """
    # Default equal weights
    if weights is None:
        weights = {
            'entropy': 0.25,
            'psnr': 0.25,
            'ssim': 0.25,
            'contrast': 0.25
        }
    
    # Use adaptive weights if provided
    if adaptive_weights is not None:
        weights = adaptive_weights
    
    # Normalize weights to ensure they sum to 1.0
    weight_sum = sum(weights.values())
    if weight_sum != 1.0:
        weights = {k: v / weight_sum for k, v in weights.items()}
    
    # Normalize metrics to [0, 1] range
    normalized = normalize_metrics(metrics_dict)
    
    # Compute composite scores
    scores = {}
    for method_name in metrics_dict:
        method_metrics = normalized[method_name]
        
        # Weighted sum: Score = Σ(weight_i * metric_i)
        score = sum(
            weights.get(metric_name, 0) * value
            for metric_name, value in method_metrics.items()
        )
        
        scores[method_name] = float(score)
    
    # Find best method
    best_method = max(scores.items(), key=lambda x: x[1])
    
    return {
        'best_method': best_method[0],
        'best_score': best_method[1],
        'all_scores': scores,
        'normalized_metrics': normalized,
        'weights_used': weights
    }


def compute_adaptive_weights(image, metrics_dict=None):
    """
    Compute adaptive weights based on image characteristics.
    
    Adjusts weights dynamically based on image properties:
    - Low brightness images: Increase entropy and contrast weights
    - High noise images: Increase SSIM weight
    - Normal images: Use balanced equal weights
    
    Parameters
    ----------
    image : np.ndarray
        Input image for analysis
    metrics_dict : dict, optional
        Metrics for adaptive adjustment. If None, uses basic approach.
        
    Returns
    -------
    dict
        Adaptive weights for each metric
        
    Notes
    -----
    - Implements simple classical measures (no deep learning)
    - Based on image statistics (brightness, variance)
    """
    import cv2
    from skimage.color import rgb2gray
    
    # Convert to grayscale
    if len(image.shape) == 3:
        image_gray = rgb2gray(image)
        image_gray = np.uint8(image_gray * 255)
    else:
        image_gray = np.uint8(image)
    
    # Analyze image properties
    mean_brightness = np.mean(image_gray)
    std_dev = np.std(image_gray)
    
    # Compute Laplacian for edge/noise detection
    laplacian = cv2.Laplacian(image_gray, cv2.CV_64F)
    noise_estimate = np.std(laplacian)
    
    # Initialize with balanced weights
    weights = {
        'entropy': 0.25,
        'psnr': 0.25,
        'ssim': 0.25,
        'contrast': 0.25
    }
    
    # Adjust weights based on image characteristics
    if mean_brightness < 100:  # Dark image
        # Increase entropy and contrast weights
        weights['entropy'] = 0.35
        weights['contrast'] = 0.30
        weights['psnr'] = 0.20
        weights['ssim'] = 0.15
    
    if noise_estimate > 25:  # Noisy image
        # Increase SSIM weight (structural preservation)
        weights['ssim'] = 0.35
        weights['entropy'] = 0.25
        weights['contrast'] = 0.20
        weights['psnr'] = 0.20
    
    if std_dev < 30:  # Low contrast image
        # Increase contrast and entropy weights
        weights['contrast'] = 0.35
        weights['entropy'] = 0.30
        weights['psnr'] = 0.20
        weights['ssim'] = 0.15
    
    # Normalize weights
    weight_sum = sum(weights.values())
    weights = {k: v / weight_sum for k, v in weights.items()}
    
    return weights
