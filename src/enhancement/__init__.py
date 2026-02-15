"""
Enhancement techniques module.
Provides various image enhancement methods.
"""
from .histogram_equalization import apply_histogram_equalization
from .clahe import apply_clahe
from .gamma_correction import apply_gamma_correction
from .bilateral_filter import apply_bilateral_filter

__all__ = [
    'apply_histogram_equalization',
    'apply_clahe',
    'apply_gamma_correction',
    'apply_bilateral_filter'
]
