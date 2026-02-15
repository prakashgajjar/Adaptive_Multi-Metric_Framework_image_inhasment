"""
Table Export Utility
Exports metrics and results to CSV format for analysis and reporting.
"""

import csv
from pathlib import Path
import pandas as pd


def export_metrics_to_csv(all_results, output_dir):
    """
    Export all metrics and results to CSV tables.
    
    Creates comprehensive CSV files including:
    1. Per-image detailed metrics
    2. Summary table across all images
    3. Best methods summary
    
    Parameters
    ----------
    all_results : dict
        Results from processing all images:
        {
            'image_name': {
                'original_image': np.ndarray,
                'enhanced_images': dict,
                'metrics': dict,
                'normalized_metrics': dict,
                'composite_scores': dict,
                'best_method': str,
                'best_score': float,
                'weights': dict
            },
            ...
        }
    output_dir : str or Path
        Directory to save CSV files
        
    Returns
    -------
    dict
        Paths to created CSV files:
        {
            'detailed_metrics': str,
            'summary': str,
            'best_methods': str
        }
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Detailed metrics for each image
    detailed_rows = []
    for image_name, result in all_results.items():
        metrics = result['metrics']
        normalized = result['normalized_metrics']
        scores = result['composite_scores']
        
        for method_name in metrics:
            row = {
                'Image': image_name,
                'Method': method_name,
                'Entropy (raw)': metrics[method_name]['entropy'],
                'PSNR (raw)': metrics[method_name]['psnr'],
                'SSIM (raw)': metrics[method_name]['ssim'],
                'Contrast (raw)': metrics[method_name]['contrast'],
                'Entropy (norm)': normalized[method_name]['entropy'],
                'PSNR (norm)': normalized[method_name]['psnr'],
                'SSIM (norm)': normalized[method_name]['ssim'],
                'Contrast (norm)': normalized[method_name]['contrast'],
                'Composite Score': scores[method_name],
                'Is Best': method_name == result['best_method']
            }
            detailed_rows.append(row)
    
    detailed_df = pd.DataFrame(detailed_rows)
    detailed_file = output_path / 'detailed_metrics.csv'
    detailed_df.to_csv(detailed_file, index=False)
    print(f"Saved detailed metrics: {detailed_file}")
    
    # 2. Summary table (one row per image)
    summary_rows = []
    for image_name, result in all_results.items():
        metrics = result['metrics']
        scores = result['composite_scores']
        
        # Calculate average metrics across all methods
        avg_metrics = {}
        for metric_name in metrics[next(iter(metrics))]:
            values = [metrics[m][metric_name] for m in metrics]
            avg_metrics[metric_name] = sum(values) / len(values)
        
        # Calculate average score
        avg_score = sum(scores.values()) / len(scores)
        
        row = {
            'Image': image_name,
            'Best Method': result['best_method'],
            'Best Score': result['best_score'],
            'Average Score': avg_score,
            'Best Entropy': max(m['entropy'] for m in metrics.values()),
            'Best PSNR': max(m['psnr'] for m in metrics.values()),
            'Best SSIM': max(m['ssim'] for m in metrics.values()),
            'Best Contrast': max(m['contrast'] for m in metrics.values()),
        }
        summary_rows.append(row)
    
    summary_df = pd.DataFrame(summary_rows)
    summary_file = output_path / 'summary.csv'
    summary_df.to_csv(summary_file, index=False)
    print(f"Saved summary: {summary_file}")
    
    # 3. Best methods summary
    best_methods_rows = []
    method_win_count = {}
    
    for image_name, result in all_results.items():
        best = result['best_method']
        method_win_count[best] = method_win_count.get(best, 0) + 1
    
    for method, count in sorted(method_win_count.items(),
                                key=lambda x: x[1], reverse=True):
        total_images = len(all_results)
        percentage = (count / total_images) * 100
        best_methods_rows.append({
            'Enhancement Method': method,
            'Times Best': count,
            'Total Images': total_images,
            'Win Percentage': f"{percentage:.1f}%"
        })
    
    best_df = pd.DataFrame(best_methods_rows)
    best_file = output_path / 'best_methods_summary.csv'
    best_df.to_csv(best_file, index=False)
    print(f"Saved best methods summary: {best_file}")
    
    return {
        'detailed_metrics': str(detailed_file),
        'summary': str(summary_file),
        'best_methods': str(best_file)
    }


def export_image_metrics_csv(image_name, metrics_dict, output_file):
    """
    Export metrics for a single image to CSV.
    
    Parameters
    ----------
    image_name : str
        Name of the image
    metrics_dict : dict
        Metrics from all methods:
        {
            'method_name': {
                'entropy': float,
                'psnr': float,
                'ssim': float,
                'contrast': float
            },
            ...
        }
    output_file : str or Path
        Output CSV file path
    """
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    rows = []
    for method, metrics in metrics_dict.items():
        row = {
            'Image': image_name,
            'Method': method,
            **metrics
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"Saved image metrics CSV: {output_file}")
