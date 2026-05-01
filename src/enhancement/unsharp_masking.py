"""
Unsharp Masking Algorithm
Enhances fine details and edges by subtracting a blurred version of the image from itself.
"""
import cv2
import numpy as np

def apply_unsharp_masking(image):
    """
    Apply unsharp masking to enhance image details.
    
    Parameters
    ----------
    image : np.ndarray
        Input image (BGR or grayscale)
        
    Returns
    -------
    np.ndarray
        Sharpened image
    """
    # Create blurred version
    gaussian = cv2.GaussianBlur(image, (0, 0), 2.0)
    
    # Calculate unsharp mask
    # We want: image * 1.5 - gaussian * 0.5
    sharpened = cv2.addWeighted(image, 1.5, gaussian, -0.5, 0)
    
    return sharpened
