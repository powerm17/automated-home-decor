import os
from flask_cors import CORS
from flask import Flask, request, jsonify
import sys
sys.path.append(r'D:\Portfolio\HomeDecorApp\automated-home-decor\models\src')  # Add the path to objectDetection
from objectDetection import detect_furniture_in_image, extract_colors_from_image
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Suggested items (can be linked to real products later)
suggested_items = {
    'chair': ['Modern Chair - $199', 'Vintage Chair - $249'],
    'couch': ['Leather Sofa - $499', 'Fabric Sofa - $399'],
    'dining table': ['Wooden Dining Table - $399', 'Glass Dining Table - $299'],
    'bed': ['King Size Bed - $599', 'Queen Size Bed - $499'],
    'potted plant': ['Succulent Plant - $19', 'Cactus Plant - $25'],
    'vase': ['Ceramic Vase - $35', 'Glass Vase - $40'],
}

@app.route('/')
def home():
    return "Welcome to the Home Decor App!"

@app.route('/upload', methods=['POST'])
def upload_image():
    # Ensure there's an image in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded image temporarily
    file_path = 'uploaded_image.jpg'
    file.save(file_path)
    
    # Perform object detection
    detected_furniture = detect_furniture_in_image(file_path)
    
    # Extract prominent colors from the image
    prominent_colors = extract_colors_from_image(file_path)
    
      # Send back suggestions based on detected furniture
    suggestions = {}
    for item in detected_furniture:
        # Use a default if no suggestions are found for the item
        suggestions[item] = suggested_items.get(item.lower(), ['No suggestions available'])
    
    return jsonify({
        'detected_furniture': detected_furniture,
        'prominent_colors': prominent_colors,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
