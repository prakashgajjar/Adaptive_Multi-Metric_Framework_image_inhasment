"""
Metric Normalization
Scales metric values to a common range for fair comparison.
"""

import numpy as np


def normalize_metrics(metrics_dict, method='minmax'):
    """
    Normalize metric values using Min-Max scaling.
    
    Min-Max normalization scales each metric to [0, 1] range based on
    the min and max values across all enhancement methods for that metric.
    This allows fair comparison and weighted combination of different metrics.
    
    Normalization formula (Min-Max):
        X_normalized = (X - X_min) / (X_max - X_min)
    Handles X_max == X_min case by returning 0.5 (neutral score).
    
    Parameters
    ----------
    metrics_dict : dict
        Dictionary with structure:
        {
            'method_name': {
                'entropy': float,
                'psnr': float,
                'ssim': float,
                'contrast': float
            },
            ...
        }
    method : str, optional
        Normalization method. Currently only 'minmax' supported.
        Default: 'minmax'
        
    Returns
    -------
    dict
        Normalized metrics with same structure as input, values in [0, 1]
        
    Raises
    ------
    ValueError
        If metrics_dict is empty or has invalid structure
        
    Notes
    -----
    - Handles edge case where all values are identical (max == min)
    - Returns neutral score (0.5) for constant metrics
    - Preserves relative ordering and differences
    """
    if not metrics_dict:
        raise ValueError("metrics_dict cannot be empty")
    
    # Extract metric names from first method
    first_method = next(iter(metrics_dict.values()))
    metric_names = list(first_method.keys())
    
    normalized = {}
    
    for metric_name in metric_names:
        # Get all values for this metric across all methods
        metric_values = [
            metrics_dict[method][metric_name]
            for method in metrics_dict
        ]
        
        metric_values = np.array(metric_values, dtype=np.float64)
        
        # Find min and max
        min_val = np.min(metric_values)
        max_val = np.max(metric_values)
        
        # Normalize each method's metric
        for method_name in metrics_dict:
            if method_name not in normalized:
                normalized[method_name] = {}
            
            value = metrics_dict[method_name][metric_name]
            
            # Handle case where all values are identical
            if max_val == min_val:
                # All same value: assign neutral score
                normalized_value = 0.5
            else:
                # Standard Min-Max normalization
                normalized_value = (value - min_val) / (max_val - min_val)
            
            normalized[method_name][metric_name] = float(
                np.clip(normalized_value, 0.0, 1.0)
            )
    
    return normalized


def get_metric_ranges(metrics_dict):
    """
    Get the min-max ranges for each metric.
    
    Useful for understanding metric value distributions and
    determining appropriate weights.
    
    Parameters
    ----------
    metrics_dict : dict
        Dictionary with metric values from all methods
        
    Returns
    -------
    dict
        Dictionary with metric ranges:
        {
            'metric_name': {'min': float, 'max': float, 'range': float},
            ...
        }
    """
    ranges = {}
    
    first_method = next(iter(metrics_dict.values()))
    metric_names = list(first_method.keys())
    
    for metric_name in metric_names:
        values = np.array([
            metrics_dict[method][metric_name]
            for method in metrics_dict
        ])
        
        ranges[metric_name] = {
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'range': float(np.max(values) - np.min(values)),
            'mean': float(np.mean(values))
        }
    
    return ranges
