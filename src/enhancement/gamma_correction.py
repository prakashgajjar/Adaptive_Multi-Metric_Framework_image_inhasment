"""
Gamma Correction Enhancement
Adjusts image brightness by applying power-law transformation.
"""

import cv2
import numpy as np


def apply_gamma_correction(image, gamma=1.2):
    """
    Apply gamma correction to adjust image brightness.
    
    Gamma correction applies a non-linear power transformation to pixel
    intensities: output = input^(1/gamma). This brightens or darkens the
    image while preserving relative differences.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). Shape: (H, W) or (H, W, C)
    gamma : float, optional
        Gamma value for correction. Default: 1.2
        - gamma < 1.0: brightens the image
        - gamma > 1.0: darkens the image
        - gamma = 1.0: no change
        
    Returns
    -------
    np.ndarray
        Gamma-corrected image with same shape and dtype as input.
        
    Notes
    -----
    - Gamma values typically range from 0.4 to 2.5
    - Default gamma=1.2 brightens dark images slightly
    - Returns numpy array with uint8 dtype
    """
    image = np.array(image, dtype=np.float32) / 255.0
    
    # Apply gamma correction: output = input^(1/gamma)
    corrected = np.power(image, 1.0 / gamma)
    
    # Convert back to 0-255 range
    enhanced = np.uint8(np.clip(corrected * 255.0, 0, 255))
    
    return enhanced
