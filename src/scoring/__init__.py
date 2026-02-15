"""
Scoring module.
Provides normalization and composite scoring.
"""
from .normalization import normalize_metrics
from .composite_score import compute_composite_score, compute_adaptive_weights

__all__ = [
    'normalize_metrics',
    'compute_composite_score',
    'compute_adaptive_weights'
]
