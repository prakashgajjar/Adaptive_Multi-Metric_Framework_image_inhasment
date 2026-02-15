"""
CLAHE (Contrast Limited Adaptive Histogram Equalization)
Advanced histogram equalization that prevents over-amplification of noise.
"""

import cv2
import numpy as np


def apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Apply CLAHE enhancement to the image.
    
    CLAHE (Contrast Limited Adaptive Histogram Equalization) performs
    histogram equalization on small image regions (tiles) with a limit
    on contrast amplification. This prevents excessive noise amplification.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). Shape: (H, W) or (H, W, C)
    clip_limit : float, optional
        Contrast limiting threshold. Default: 2.0
        Higher values allow more contrast enhancement.
    tile_grid_size : tuple, optional
        Grid size for local histogram equalization. Default: (8, 8)
        
    Returns
    -------
    np.ndarray
        Enhanced image with same shape and dtype as input.
        
    Notes
    -----
    - For color images, applies CLAHE to brightness in HSV space
    - Prevents noise amplification through contrast limiting
    - Returns numpy array with uint8 dtype
    """
    image = np.array(image, dtype=np.uint8)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    if len(image.shape) == 2:
        # Grayscale image
        enhanced = clahe.apply(image)
    else:
        # Color image - apply CLAHE to brightness channel
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.uint8)
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return enhanced
