"""
SSIM (Structural Similarity Index) Metric
Measures perceived structural similarity between images.
"""

import numpy as np
from skimage.color import rgb2gray
from skimage.metrics import structural_similarity as ski_ssim


def calculate_ssim(image_enhanced, image_original=None, data_range=255):
    """
    Calculate Structural Similarity Index (SSIM).
    
    SSIM measures structural similarity between two images, correlating
    better with human perception than PSNR. Higher SSIM indicates greater
    structural similarity.
    
    Mathematical definition:
        SSIM = (2*μ_x*μ_y + C1) * (2*σ_xy + C2) / 
               ((μ_x^2 + μ_y^2 + C1) * (σ_x^2 + σ_y^2 + C2))
    where μ = mean, σ = variance, σ_xy = covariance, C1,C2 = stabilization constants.
    
    Parameters
    ----------
    image_enhanced : np.ndarray
        Enhanced image to evaluate
    image_original : np.ndarray, optional
        Original reference image for comparison. If None, uses self-similarity.
        Default: None
    data_range : int, optional
        Maximum possible pixel value. Default: 255
        
    Returns
    -------
    float
        SSIM score. Range: -1 to 1 (typically 0 to 1)
        Higher values = greater structural similarity.
        1.0 = identical images
        
    Notes
    -----
    - Better matches human visual perception than PSNR
    - Requires reference image to be meaningful
    - If no reference, uses internal consistency metric
    """
    image_enhanced = np.array(image_enhanced, dtype=np.float64)
    
    # Convert to grayscale if needed
    if len(image_enhanced.shape) == 3:
        image_enhanced = rgb2gray(image_enhanced)
    
    if image_original is not None:
        # Reference-based SSIM
        image_original = np.array(image_original, dtype=np.float64)
        if len(image_original.shape) == 3:
            image_original = rgb2gray(image_original)
        
        # Use scikit-image SSIM calculation
        ssim_value = ski_ssim(
            image_original,
            image_enhanced,
            data_range=data_range
        )
    else:
        # Reference-free: Use self-similarity metric
        # Calculate local feature patches and measure consistency
        h, w = image_enhanced.shape
        patch_size = min(8, h // 4, w // 4)
        
        if patch_size < 2:
            # Image too small, return normalized variance
            return float(np.clip(1.0 - np.var(image_enhanced) / 255**2, 0, 1))
        
        # Extract overlapping patches and compute their consistency
        patches = []
        for i in range(0, h - patch_size, patch_size):
            for j in range(0, w - patch_size, patch_size):
                patch = image_enhanced[i:i+patch_size, j:j+patch_size].flatten()
                patches.append(patch)
        
        if len(patches) < 2:
            ssim_value = 1.0
        else:
            # high patch correlation indicates consistent structure
            patches_array = np.array(patches)
            mean_patch_similarity = np.mean([
                np.corrcoef(patches_array[i], patches_array[j])[0, 1]
                for i in range(min(10, len(patches)))
                for j in range(i+1, min(i+3, len(patches)))
            ])
            ssim_value = np.clip(mean_patch_similarity, 0, 1)
    
    return float(np.clip(ssim_value, -1, 1))
