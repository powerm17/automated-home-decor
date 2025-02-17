#app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights='imagenet')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Image not processed correctly"}), 400

    img_resized = cv2.resize(img, (224, 224))
    img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(img_resized)
    predictions = model.predict(np.expand_dims(img_preprocessed, axis=0))

    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)[0]
    
    result = []
    for pred in decoded_predictions:
        result.append({
            'class': pred[1],  # Class name
            'confidence': float(pred[2])  # Confidence score
        })
    
    # Return the predictions as JSON
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)
