# app.py

from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained MobileNetV2 model (Might replace with custom model)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Define the /upload route to accept images
@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the image from the POST request
    file = request.files['image']
    
    # Read the image using OpenCV
    img_array = np.frombuffer(file.read(), np.uint8)  # Convert the image buffer to a numpy array
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Decode the image
    
    # Check if the image is read successfully
    if img is None:
        return jsonify({"error": "Image not processed correctly"}), 400
    
    # Pre-process the image (resize and normalize)
    img_resized = cv2.resize(img, (224, 224))  # Resize the image to 224x224
    img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(img_resized)  # Model MobileNetV2 pre-processing
    
    # Run object recognition on the image
    predictions = model.predict(np.expand_dims(img_preprocessed, axis=0))  # Expand the dims to match input format
    
    # Decode predictions (MobileNetV2 outputs a prediction vector)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)[0]
    
    # Prepare a result dictionary with predictions
    result = []
    for pred in decoded_predictions:
        result.append({
            'class': pred[1],
            'confidence': float(pred[2])  # Convert confidence to a float for JSON serialization
        })
    
    # Return the predictions as JSON
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
