"""
Bilateral Filtering Enhancement
Edge-preserving smoothing that reduces noise and improves clarity.
"""

import cv2
import numpy as np


def apply_bilateral_filter(image, diameter=9, sigma_color=75, sigma_space=75):
    """
    Apply bilateral filtering for noise reduction and edge preservation.
    
    Bilateral filtering performs weighted averaging where weights depend
    on both spatial distance and photometric similarity. This preserves
    edges while reducing noise.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). Shape: (H, W) or (H, W, C)
    diameter : int, optional
        Diameter of pixel neighborhood. Default: 9
        Larger values include more neighbors (slower).
    sigma_color : float, optional
        Standard deviation for color space. Default: 75
        Larger values blur more similar colors together.
    sigma_space : float, optional
        Standard deviation for spatial domain. Default: 75
        Larger values affect more distant pixels.
        
    Returns
    -------
    np.ndarray
        Filtered image with same shape and dtype as input.
        
    Notes
    -----
    - Excellent for noise reduction while preserving edges
    - More computationally expensive than other filters
    - Works on both grayscale and color images
    - Returns numpy array with uint8 dtype
    """
    image = np.array(image, dtype=np.uint8)
    
    # Apply bilateral filter
    enhanced = cv2.bilateralFilter(
        image,
        d=diameter,
        sigmaColor=sigma_color,
        sigmaSpace=sigma_space
    )
    
    return enhanced
