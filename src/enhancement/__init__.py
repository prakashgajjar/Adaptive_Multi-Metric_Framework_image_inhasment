"""
Enhancement techniques module.
Provides various image enhancement methods.
"""
from .histogram_equalization import apply_histogram_equalization
from .clahe import apply_clahe
from .gamma_correction import apply_gamma_correction
from .bilateral_filter import apply_bilateral_filter
from .unsharp_masking import apply_unsharp_masking
from .hybrid_enhancement import apply_hybrid_enhancement

__all__ = [
    'apply_histogram_equalization',
    'apply_clahe',
    'apply_gamma_correction',
    'apply_bilateral_filter',
    'apply_unsharp_masking',
    'apply_hybrid_enhancement'
]
