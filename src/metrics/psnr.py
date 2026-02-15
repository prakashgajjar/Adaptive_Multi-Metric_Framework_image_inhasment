"""
PSNR (Peak Signal-to-Noise Ratio) Metric
Measures fidelity between or quality of image.
"""

import numpy as np
from skimage.color import rgb2gray


def calculate_psnr(image_enhanced, image_original=None, data_range=255):
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR).
    
    PSNR measures the ratio of maximum possible power to corrupting noise
    power. Higher PSNR indicates better quality/fidelity.
    
    Mathematical definition:
        PSNR = 10 * log10((MAX^2) / MSE)
    where MAX is maximum intensity value (255 for 8-bit), MSE is Mean Squared Error.
    
    Parameters
    ----------
    image_enhanced : np.ndarray
        Enhanced image to evaluate
    image_original : np.ndarray, optional
        Original reference image. If None, uses basic quality metric.
        Default: None
    data_range : int, optional
        Maximum possible pixel value. Default: 255
        
    Returns
    -------
    float
        PSNR in decibels (dB). Typical range: 20-50 dB.
        Higher values = better quality.
        
    Notes
    -----
    - When original image is None, calculates variance-based PSNR
    - With original image, calculates fidelity to reference
    - Typical values: < 20 dB = poor, 20-30 dB = fair, > 40 dB = excellent
    """
    image_enhanced = np.array(image_enhanced, dtype=np.float64)
    
    # Convert to grayscale if needed
    if len(image_enhanced.shape) == 3:
        image_enhanced = rgb2gray(image_enhanced)
    
    if image_original is not None:
        # Reference-based PSNR: Compare with original
        image_original = np.array(image_original, dtype=np.float64)
        if len(image_original.shape) == 3:
            image_original = rgb2gray(image_original)
        
        # Calculate Mean Squared Error
        mse = np.mean((image_enhanced - image_original) ** 2)
        
        if mse == 0:
            # Images are identical
            return 100.0
    else:
        # Reference-free PSNR: Use variance as proxy
        # PSNR ~ 10 * log10(data_range^2 / variance)
        mse = np.var(image_enhanced)
        if mse == 0:
            return 50.0
    
    # Prevent division by zero
    if mse < 1e-10:
        return 100.0
    
    # Calculate PSNR: 10 * log10(MAX^2 / MSE)
    psnr = 10.0 * np.log10((data_range ** 2) / mse)
    
    return float(psnr)
