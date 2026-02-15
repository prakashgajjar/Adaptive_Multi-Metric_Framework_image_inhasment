"""
Histogram Equalization Enhancement
Redistributes image intensity values uniformly to improve contrast.
"""

import cv2
import numpy as np


def apply_histogram_equalization(image):
    """
    Apply histogram equalization to enhance image contrast.
    
    Histogram equalization redistributes pixel intensities to spread the
    histogram uniformly across the intensity range. This improves contrast
    especially in low-contrast images.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). Shape: (H, W) or (H, W, C)
        
    Returns
    -------
    np.ndarray
        Enhanced image with same shape and dtype as input.
        
    Notes
    -----
    - For color images, applies CLAHE-based enhancement to preserve colors
    - For grayscale, uses standard histogram equalization
    - Returns numpy array with uint8 dtype
    """
    image = np.array(image, dtype=np.uint8)
    
    if len(image.shape) == 2:
        # Grayscale image
        enhanced = cv2.equalizeHist(image)
    else:
        # Color image - equalize only brightness channel (V in HSV)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2].astype(np.uint8))
        enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    return enhanced
