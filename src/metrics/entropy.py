"""
Entropy Metric
Measures information content and detail richness of an image.
"""

import numpy as np
from skimage.color import rgb2gray


def calculate_entropy(image):
    """
    Calculate Shannon entropy of the image.
    
    Shannon entropy measures the average information content or disorder
    in the image. Higher entropy indicates more information/detail richness.
    Used to assess image clarity and detail.
    
    Mathematical definition:
        H = -Σ(p_i * log2(p_i))
    where p_i is the probability of intensity i (normalized histogram).
    
    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). Shape: (H, W) or (H, W, C)
        
    Returns
    -------
    float
        Entropy value in bits. Typical range: 0-8 for 8-bit images.
        Higher values = more information content.
        
    Notes
    -----
    - Higher entropy usually indicates clearer, more detailed images
    - Useful for evaluating enhancement effectiveness
    - Invariant to image scaling
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        image_gray = rgb2gray(image)
        image_gray = np.uint8(image_gray * 255)
    else:
        image_gray = np.uint8(image)
    
    # Calculate histogram (probability distribution)
    hist, _ = np.histogram(image_gray, bins=256, range=(0, 256))
    hist = hist / hist.sum()  # Normalize to get probabilities
    
    # Remove zero probabilities to avoid log(0)
    hist = hist[hist > 0]
    
    # Calculate entropy: H = -Σ(p_i * log2(p_i))
    entropy = -np.sum(hist * np.log2(hist))
    
    return float(entropy)
