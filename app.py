import os
import sys
import base64
import io
from pathlib import Path

# Force UTF-8 encoding for standard output to avoid charmap errors on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2

# Import the existing framework
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from main import AdaptiveImageEnhancement

app = Flask(__name__)
# Enable CORS for frontend integration
CORS(app)

def encode_image_base64(image):
    """Encodes a numpy image array to base64 string"""
    # Check if image is float or int, convert to uint8
    if image.dtype != np.uint8:
        if image.max() <= 1.0:
            image = (image * 255).astype(np.uint8)
        else:
            image = image.astype(np.uint8)
            
    # Ensure it's in BGR format for cv2.imencode if it's RGB
    # The existing code likely uses OpenCV which natively uses BGR. 
    # Let's assume the image is single channel or BGR as per OpenCV standard.
    is_success, buffer = cv2.imencode(".png", image)
    if is_success:
        io_buf = io.BytesIO(buffer)
        encoded_img = base64.b64encode(io_buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{encoded_img}"
    return None

@app.route('/api/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
        
    use_adaptive = request.form.get('adaptive', 'false').lower() == 'true'

    try:
        # Read the image file into a numpy array
        in_memory_file = io.BytesIO(file.read())
        file_bytes = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # The original framework uses cv2.imread which defaults to BGR color
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
             return jsonify({'error': 'Invalid image format'}), 400

        # Create framework instance (we don't need output/results dirs as we won't save files)
        # We will patch the save methods or just use a dummy dir
        dummy_dir = PROJECT_ROOT / 'temp_run'
        framework = AdaptiveImageEnhancement(
            input_dir=dummy_dir, 
            output_dir=dummy_dir, 
            results_dir=dummy_dir, 
            use_adaptive_weights=use_adaptive
        )
        
        # We only want to process the image and get results, we don't want to save anything.
        # Let's extract the core processing logic from process_image without the save steps.
        image_name = file.filename
        
        # 1. Enhance
        enhanced_images = framework.enhance_image(image_name, image)
        
        # 2. Compute metrics
        metrics = framework.compute_metrics(image_name, image, enhanced_images)
        
        # 3. Score
        scoring_result = framework.score_enhancements(image_name, image, metrics)
        
        # Convert all images to Base64
        original_b64 = encode_image_base64(image)
        enhanced_b64 = {}
        for method, img in enhanced_images.items():
            enhanced_b64[method] = encode_image_base64(img)
            
        best_method = scoring_result['best_method']
        
        # Construct response
        response_data = {
            'original_image': original_b64,
            'enhanced_images': enhanced_b64,
            'best_method': best_method,
            'best_image': enhanced_b64[best_method],
            'metrics': metrics,
            'normalized_metrics': scoring_result['normalized_metrics'],
            'composite_scores': scoring_result['all_scores'],
            'weights': scoring_result['weights_used']
        }
        
        return jsonify(response_data)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
