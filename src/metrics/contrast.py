"""
Contrast Metric
Measures image contrast using standard deviation of intensities.
"""

import numpy as np
from skimage.color import rgb2gray


def calculate_contrast(image):
    """
    Calculate image contrast using standard deviation of pixel intensities.
    
    Contrast measures the spread of pixel intensities. Higher contrast
    means greater difference between light and dark regions, indicating
    better visual distinction and clarity.
    
    Mathematical definition:
        Contrast = σ = sqrt(E[(X - μ)^2])
    where μ = mean intensity, X = pixel values.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). Shape: (H, W) or (H, W, C)
        
    Returns
    -------
    float
        Contrast value (standard deviation). Typical range: 0-255.
        Higher values = higher contrast.
        
    Notes
    -----
    - Simple but effective contrast measure
    - Normalized by image intensity range
    - Works well for detecting quality improvements
    - Invariant to translations but sensitive to scaling
    """
    # Convert to grayscale if needed
    image = np.array(image, dtype=np.float64)
    
    if len(image.shape) == 3:
        image_gray = rgb2gray(image)
    else:
        image_gray = image / 255.0 if np.max(image) > 1 else image
    
    # Normalize to [0, 1] range if needed
    if np.max(image_gray) > 1:
        image_gray = image_gray / 255.0
    
    # Calculate standard deviation (contrast measure)
    contrast = np.std(image_gray)
    
    # Scale back to 0-255 range for consistency
    contrast_scaled = contrast * 255
    
    return float(contrast_scaled)
