"""
Adaptive Image Enhancement Framework - Main Pipeline

Complete orchestration of the image enhancement and evaluation system.
Processes images through multiple enhancement techniques, evaluates quality
metrics, computes composite scores, and selects optimal enhancements.
"""

import os
import sys
from pathlib import Path
import numpy as np
import argparse
from datetime import datetime

# Add src to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

# Import enhancement techniques
from enhancement import (
    apply_histogram_equalization,
    apply_clahe,
    apply_gamma_correction,
    apply_bilateral_filter,
    apply_unsharp_masking,
    apply_hybrid_enhancement
)

# Import metrics
from metrics import (
    calculate_entropy,
    calculate_psnr,
    calculate_ssim,
    calculate_contrast
)

# Import scoring
from scoring import (
    normalize_metrics,
    compute_composite_score,
    compute_adaptive_weights
)

# Import utilities
from utils import (
    load_images,
    save_image,
    visualize_comparison,
    plot_metrics,
    export_metrics_to_csv
)


class AdaptiveImageEnhancement:
    """
    Main enhancement framework orchestrator.
    
    Manages the complete pipeline for adaptive image enhancement:
    1. Load images
    2. Apply multiple enhancement techniques
    3. Compute quality metrics
    4. Normalize and score results
    5. Select best enhancement
    6. Generate visualizations and reports
    """
    
    def __init__(self, input_dir, output_dir, results_dir, use_adaptive_weights=False):
        """
        Initialize the enhancement framework.
        
        Parameters
        ----------
        input_dir : str or Path
            Directory containing input images
        output_dir : str or Path
            Directory for saving enhanced images
        results_dir : str or Path
            Directory for saving results, graphs, and tables
        use_adaptive_weights : bool, optional
            Whether to use adaptive weight selection based on image
            characteristics. Default: False (uses equal weights)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.results_dir = Path(results_dir)
        self.use_adaptive_weights = use_adaptive_weights
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        (self.results_dir / 'graphs').mkdir(parents=True, exist_ok=True)
        (self.results_dir / 'comparison_tables').mkdir(parents=True, exist_ok=True)
        (self.results_dir / 'best_outputs').mkdir(parents=True, exist_ok=True)
        
        # Enhancement methods mapping
        self.enhancement_methods = {
            'histogram_equalization': apply_histogram_equalization,
            'clahe': apply_clahe,
            'gamma_correction': apply_gamma_correction,
            'bilateral_filter': apply_bilateral_filter,
            'unsharp_masking': apply_unsharp_masking,
            'hybrid_enhancement': apply_hybrid_enhancement
        }
        
        # Metric functions mapping
        self.metric_functions = {
            'entropy': calculate_entropy,
            'psnr': calculate_psnr,
            'ssim': calculate_ssim,
            'contrast': calculate_contrast
        }
        
        self.all_results = {}
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def enhance_image(self, image_name, image):
        """
        Apply all enhancement techniques to an image.
        
        Parameters
        ----------
        image_name : str
            Name of the image (for tracking)
        image : np.ndarray
            Input image array
            
        Returns
        -------
        dict
            Enhancement results for all methods
        """
        print(f"\n{'='*70}")
        print(f"Processing: {image_name}")
        print(f"{'='*70}")
        
        enhanced_images = {}
        
        for method_name, method_fn in self.enhancement_methods.items():
            print(f"  • Applying {method_name}...", end=' ')
            try:
                enhanced = method_fn(image)
                enhanced_images[method_name] = enhanced
                print("✓")
            except Exception as e:
                print(f"✗ Error: {e}")
                enhanced_images[method_name] = image  # Fallback to original
        
        return enhanced_images
    
    def compute_metrics(self, image_name, original_image, enhanced_images):
        """
        Compute quality metrics for all enhanced images.
        
        Parameters
        ----------
        image_name : str
            Name of the image
        original_image : np.ndarray
            Original input image
        enhanced_images : dict
            Dictionary of enhanced images from all methods
            
        Returns
        -------
        dict
            Computed metrics for each method
        """
        print("\n  Computing metrics:")
        metrics = {}
        
        for method_name, enhanced_image in enhanced_images.items():
            print(f"    • {method_name}...", end=' ')
            try:
                metrics[method_name] = {
                    'entropy': calculate_entropy(enhanced_image),
                    'psnr': calculate_psnr(enhanced_image, original_image),
                    'ssim': calculate_ssim(enhanced_image, original_image),
                    'contrast': calculate_contrast(enhanced_image)
                }
                print("✓")
            except Exception as e:
                print(f"✗ Error: {e}")
                metrics[method_name] = {
                    'entropy': 0,
                    'psnr': 0,
                    'ssim': 0,
                    'contrast': 0
                }
        
        return metrics
    
    def score_enhancements(self, image_name, original_image, metrics):
        """
        Score and rank enhancement methods.
        
        Parameters
        ----------
        image_name : str
            Name of the image
        original_image : np.ndarray
            Original image
        metrics : dict
            Computed metrics for all methods
            
        Returns
        -------
        dict
            Scoring results including best method
        """
        print("\n  Scoring enhancements:")
        
        # Determine weights
        if self.use_adaptive_weights:
            weights = compute_adaptive_weights(original_image, metrics)
            print(f"    Adaptive weights computed")
        else:
            weights = {
                'entropy': 0.25,
                'psnr': 0.25,
                'ssim': 0.25,
                'contrast': 0.25
            }
            print(f"    Using equal weights")
        
        # Compute composite scores
        scoring_result = compute_composite_score(metrics, weights=weights)
        
        print(f"    Best method: {scoring_result['best_method']} "
              f"(Score: {scoring_result['best_score']:.4f})")
        
        return scoring_result
    
    def save_results(self, image_name, original_image, enhanced_images,
                    scoring_result):
        """
        Save all enhanced images and best output.
        
        Parameters
        ----------
        image_name : str
            Name of the image
        original_image : np.ndarray
            Original image
        enhanced_images : dict
            All enhanced images
        scoring_result : dict
            Scoring results
        """
        print("\n  Saving outputs:")
        
        # Save all enhanced images
        for method_name, enhanced_image in enhanced_images.items():
            filename = f"{image_name}_{method_name}.png"
            output_path = self.output_dir / filename
            try:
                save_image(enhanced_image, self.output_dir, filename)
            except Exception as e:
                print(f"    ✗ Error saving {filename}: {e}")
        
        # Save best enhanced image
        best_method = scoring_result['best_method']
        best_image = enhanced_images[best_method]
        best_filename = f"{image_name}_BEST_{best_method}.png"
        
        try:
            save_image(best_image, self.results_dir / 'best_outputs', best_filename)
            print(f"    ✓ Saved best output: {best_filename}")
        except Exception as e:
            print(f"    ✗ Error saving best output: {e}")
    
    def generate_visualizations(self, image_name, original_image,
                               enhanced_images, scoring_result):
        """
        Generate comparison visualizations and metric plots.
        
        Parameters
        ----------
        image_name : str
            Name of the image
        original_image : np.ndarray
            Original image
        enhanced_images : dict
            All enhanced images
        scoring_result : dict
            Scoring results with metrics and scores
        """
        print("\n  Generating visualizations:")
        
        try:
            # Comparison visualization
            print(f"    • Comparison image...", end=' ')
            visualize_comparison(
                original_image,
                enhanced_images,
                image_name,
                self.results_dir / 'graphs'
            )
            print("✓")
            
            # Metrics plot
            print(f"    • Metrics plot...", end=' ')
            plot_metrics(
                scoring_result['all_scores'],
                image_name,
                self.results_dir / 'graphs',
                scoring_result['normalized_metrics']
            )
            print("✓")
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def process_image(self, image_name, image):
        """
        Complete processing pipeline for a single image.
        
        Parameters
        ----------
        image_name : str
            Name of the image
        image : np.ndarray
            Input image array
            
        Returns
        -------
        dict
            Complete results for the image
        """
        # Apply enhancements
        enhanced_images = self.enhance_image(image_name, image)
        
        # Compute metrics
        metrics = self.compute_metrics(image_name, image, enhanced_images)
        
        # Score enhancements
        scoring_result = self.score_enhancements(image_name, image, metrics)
        
        # Save results
        self.save_results(image_name, image, enhanced_images, scoring_result)
        
        # Generate visualizations
        self.generate_visualizations(image_name, image, enhanced_images,
                                    scoring_result)
        
        # Store results
        results = {
            'original_image': image,
            'enhanced_images': enhanced_images,
            'metrics': metrics,
            'normalized_metrics': scoring_result['normalized_metrics'],
            'composite_scores': scoring_result['all_scores'],
            'best_method': scoring_result['best_method'],
            'best_score': scoring_result['best_score'],
            'weights': scoring_result['weights_used']
        }
        
        self.all_results[image_name] = results
        
        return results
    
    def process_all_images(self):
        """
        Process all images in the input directory.
        
        Loads images, applies enhancements, and generates outputs for
        all images found in the input directory.
        """
        print("\n" + "="*70)
        print("ADAPTIVE IMAGE ENHANCEMENT FRAMEWORK")
        print("="*70)
        print(f"Input Directory: {self.input_dir}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Results Directory: {self.results_dir}")
        print(f"Adaptive Weights: {'Yes' if self.use_adaptive_weights else 'No'}")
        print("="*70)
        
        try:
            # Load images
            print("\nLoading images...")
            images = load_images(self.input_dir)
            print(f"Loaded {len(images)} image(s)")
            
            # Process each image
            for image_name, image in images.items():
                self.process_image(image_name, image)
            
            # Export results
            print("\n" + "="*70)
            print("EXPORTING RESULTS")
            print("="*70)
            csv_files = export_metrics_to_csv(
                self.all_results,
                self.results_dir / 'comparison_tables'
            )
            
            # Print summary
            self.print_summary()
            
            print("\n" + "="*70)
            print("PROCESSING COMPLETE")
            print("="*70)
            print(f"Results saved to: {self.results_dir}")
            
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
    
    def print_summary(self):
        """Print summary of results across all images."""
        if not self.all_results:
            return
        
        print("\nSUMMARY:")
        print("-" * 70)
        
        method_wins = {}
        
        for image_name, result in self.all_results.items():
            best_method = result['best_method']
            best_score = result['best_score']
            
            method_wins[best_method] = method_wins.get(best_method, 0) + 1
            
            print(f"\n{image_name}:")
            print(f"  Best Method: {best_method}")
            print(f"  Score: {best_score:.4f}")
            print(f"  Weights: {result['weights']}")
            
            # Print all scores
            all_scores = result['composite_scores']
            print(f"  All Scores:")
            for method, score in sorted(all_scores.items(),
                                       key=lambda x: x[1], reverse=True):
                marker = "★" if method == best_method else " "
                print(f"    {marker} {method}: {score:.4f}")
        
        print("\n" + "=" * 70)
        print("OVERALL STATISTICS:")
        print("-" * 70)
        
        total_images = len(self.all_results)
        print(f"Total Images Processed: {total_images}")
        print(f"\nMethod Win Count:")
        for method, count in sorted(method_wins.items(),
                                   key=lambda x: x[1], reverse=True):
            percentage = (count / total_images) * 100
            print(f"  {method}: {count} wins ({percentage:.1f}%)")


def main():
    """Main entry point for the enhancement framework."""
    parser = argparse.ArgumentParser(
        description='Adaptive Image Enhancement Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py data/input_images
  python main.py data/input_images --adaptive
  python main.py data/input_images --output results/enhanced --adaptive
        """
    )
    
    parser.add_argument(
        'input_dir',
        help='Directory containing input images'
    )
    
    parser.add_argument(
        '--output',
        default='data/output_images',
        help='Directory for enhanced images (default: data/output_images)'
    )
    
    parser.add_argument(
        '--results',
        default='results',
        help='Directory for results and visualizations (default: results)'
    )
    
    parser.add_argument(
        '--adaptive',
        action='store_true',
        help='Use adaptive weight selection based on image characteristics'
    )
    
    args = parser.parse_args()
    
    # Create framework instance
    framework = AdaptiveImageEnhancement(
        input_dir=args.input_dir,
        output_dir=args.output,
        results_dir=args.results,
        use_adaptive_weights=args.adaptive
    )
    
    # Process all images
    framework.process_all_images()


if __name__ == '__main__':
    main()
