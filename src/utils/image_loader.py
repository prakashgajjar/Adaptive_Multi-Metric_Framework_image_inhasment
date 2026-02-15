"""
Image Loader Utility
Handles loading and saving images with proper format handling.
"""

import os
import cv2
import numpy as np
from pathlib import Path


def load_images(directory_path):
    """
    Load all images from a directory.
    
    Recursively loads supported image formats from the specified directory.
    Supported formats: .jpg, .jpeg, .png, .bmp, .tiff
    
    Parameters
    ----------
    directory_path : str or Path
        Path to directory containing images
        
    Returns
    -------
    dict
        Dictionary with structure:
        {
            'image_filename': np.ndarray,  # Image array (H, W, C)
            ...
        }
        Image arrays are in BGR format (OpenCV convention)
        
    Raises
    ------
    FileNotFoundError
        If directory does not exist
    ValueError
        If no images found in directory
        
    Notes
    -----
    - Returns images in BGR format (use cv2.cvtColor for RGB)
    - Images are loaded as uint8 arrays
    - Filenames without path are used as dictionary keys
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    images = {}
    
    # Find all image files
    for file_path in directory.rglob('*'):
        if file_path.suffix.lower() in image_extensions:
            try:
                # Load image using OpenCV (BGR format)
                image = cv2.imread(str(file_path))
                
                if image is None:
                    print(f"Warning: Failed to load {file_path.name}")
                    continue
                
                # Use only filename as key
                images[file_path.stem] = image
                print(f"Loaded: {file_path.name} -> Shape: {image.shape}")
                
            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
    
    if not images:
        raise ValueError(
            f"No images found in {directory_path}. "
            f"Supported formats: {image_extensions}"
        )
    
    return images


def save_image(image, output_path, filename):
    """
    Save image to file with proper format handling.
    
    Parameters
    ----------
    image : np.ndarray
        Image to save (uint8 array, BGR format)
    output_path : str or Path
        Directory to save the image
    filename : str
        Filename (with extension, e.g., 'enhanced.png')
        
    Returns
    -------
    str
        Full path to saved image
        
    Raises
    ------
    ValueError
        If image is invalid or save fails
        
    Notes
    -----
    - Creates output directory if it doesn't exist
    - Supported formats: .jpg, .jpeg, .png, .bmp, .tiff
    - Automatically converts to uint8 if needed
    """
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure image is uint8
    if image.dtype != np.uint8:
        image = np.uint8(np.clip(image, 0, 255))
    
    full_path = output_dir / filename
    
    try:
        success = cv2.imwrite(str(full_path), image)
        
        if not success:
            raise ValueError(f"Failed to save image: {full_path}")
        
        print(f"Saved: {filename} to {full_path}")
        return str(full_path)
        
    except Exception as e:
        raise ValueError(f"Error saving {filename}: {e}")


def get_image_info(image):
    """
    Get information about an image.
    
    Parameters
    ----------
    image : np.ndarray
        Input image
        
    Returns
    -------
    dict
        Information about the image:
        {
            'shape': tuple,       # (H, W) or (H, W, C)
            'dtype': str,         # Data type
            'size_mb': float,     # Size in megabytes
            'is_color': bool,     # Whether image is color
            'min_val': int,       # Minimum pixel value
            'max_val': int        # Maximum pixel value
        }
    """
    return {
        'shape': image.shape,
        'dtype': str(image.dtype),
        'size_mb': image.nbytes / (1024 ** 2),
        'is_color': len(image.shape) == 3,
        'min_val': int(np.min(image)),
        'max_val': int(np.max(image))
    }
