"""
Hybrid Enhancement Algorithm (Highly Improved)
A state-of-the-art hybrid pipeline designed to produce the absolute best visual quality
without introducing artifacts or washing out colors.
"""
import cv2
import numpy as np

def apply_hybrid_enhancement(image):
    """
    Apply a highly optimized hybrid pipeline of enhancements.
    
    Pipeline Steps:
    1. Color Space Conversion (BGR -> LAB) to safely separate luminance from color.
    2. Edge-preserving Denoising (Bilateral Filter) on the Luminance channel.
    3. Adaptive Contrast Enhancement (CLAHE) on the Luminance channel.
    4. Detail Enhancement (Unsharp Masking) on the Luminance channel.
    5. Subtle Color Saturation Boost on A and B channels.
    6. Convert back to BGR.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (BGR or grayscale)
        
    Returns
    -------
    np.ndarray
        Highly enhanced image
    """
    # If grayscale, convert to BGR temporarily so we can use standard LAB pipeline
    is_gray = len(image.shape) == 2 or image.shape[2] == 1
    if is_gray:
        img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        img_bgr = image.copy()

    # Convert to LAB color space to avoid shifting colors when changing contrast
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    
    # 1. Edge-preserving Denoising on L-channel
    # Removes grain/noise from shadows but keeps sharp edges intact
    l_denoised = cv2.bilateralFilter(l_channel, d=5, sigmaColor=35, sigmaSpace=35)
    
    # 2. Local Contrast Enhancement (CLAHE) on L-channel
    # Balances lighting in heavily shadowed or over-exposed areas
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l_denoised)
    
    # 3. Detail Enhancement (Unsharp Masking) on L-channel
    # Pops micro-contrast and fine textures
    gaussian = cv2.GaussianBlur(l_clahe, (0, 0), 1.5)
    l_sharpened = cv2.addWeighted(l_clahe, 1.25, gaussian, -0.25, 0)
    
    # 4. Color Saturation Boost on A and B channels
    # Increase saturation by stretching the A and B channels slightly around 128 (neutral)
    a_channel = cv2.addWeighted(a_channel, 1.1, np.full_like(a_channel, 128), -0.1, 0)
    b_channel = cv2.addWeighted(b_channel, 1.1, np.full_like(b_channel, 128), -0.1, 0)
    
    # Merge channels back
    merged_lab = cv2.merge([l_sharpened, a_channel, b_channel])
    
    # Convert back to BGR
    final_bgr = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
    
    # Return grayscale if input was grayscale
    if is_gray:
        return cv2.cvtColor(final_bgr, cv2.COLOR_BGR2GRAY)
        
    return final_bgr
