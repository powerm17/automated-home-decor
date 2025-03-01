import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras._tf_keras.keras.applications import MobileNetV2
from keras._tf_keras.keras.preprocessing import image
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Input, Dense, Flatten
from colorthief import ColorThief
from tensorflow.python.framework.ops import convert_to_tensor
from PIL import Image  # PIL for image handling

# Ensure consistent resizing for images
def resize_image(image_path, target_size=(224, 224)):
    img = Image.open(image_path)
    img = img.resize(target_size)
    return np.array(img)

# Aesthetic classification (using MobileNetV2)
def classify_aesthetic(image_path, model):
    img_array = resize_image(image_path)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)[0]
    return decoded_predictions  # Returns the top predicted class

# Extract dominant colors (colorthief)
def extract_dominant_colors(image_path):
    color_thief = ColorThief(image_path)
    palette = color_thief.get_palette(color_count=5)  # Gets 5 most dominant colors
    return palette  # List of RGB colors

# Load object detection model (adapt as needed)
from objectDetection import load_object_detection_model, run_inference_for_single_image

# Process folder of images
def process_image_folder(image_dir, object_detection_model, aesthetic_model):
    X_images = []
    y_aesthetic = []
    y_colors = []

    # Iterate over each aesthetic folder in the dataset
    for label in os.listdir(image_dir):
        aesthetic_folder = os.path.join(image_dir, label)  # Full path to the aesthetic folder
        if os.path.isdir(aesthetic_folder):
            for img_name in os.listdir(aesthetic_folder):  # Iterate over images in this aesthetic folder
                img_path = os.path.join(aesthetic_folder, img_name)
                image = Image.open(img_path)
                image = image.convert('RGB')  # Convert to RGB

                # Check if it's a valid image file
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    try:
                        # Object detection (resize before passing to model)
                        boxes, classes, scores, masks = run_inference_for_single_image(object_detection_model, img_path)

                        # Classify the aesthetic of the room
                        aesthetic_prediction = classify_aesthetic(img_path, aesthetic_model)
                        aesthetic_label = aesthetic_prediction[0][1]  # Takes top prediction class

                        # Extract dominant colors from image
                        colors = extract_dominant_colors(img_path)

                        # Store results (images and labels)
                        img_array = resize_image(img_path) / 255.0  # Resize and normalize image
                        X_images.append(img_array)
                        y_aesthetic.append(aesthetic_label)
                        y_colors.append(colors)
                    except Exception as e:
                        print(f"Error processing {img_path}: {e}")
                        continue  # Skip this image if there was an error

    X_images = np.array(X_images)
    y_aesthetic = np.array(y_aesthetic)
    y_colors = np.array(y_colors)

    return X_images, y_aesthetic, y_colors

# Build the multi-output model
def build_multi_output_model():
    input_layer = Input(shape=(224, 224, 3))  # Ensure images are 224x224x3
    x = Flatten()(input_layer)
    x = Dense(256, activation='relu')(x)

    # Aesthetic classification output
    aesthetic_output = Dense(3, activation='softmax', name='aesthetic')(x)  # Change number of classes as per requirement

    # Color palette regression output (5 colors, 3 RGB channels each)
    color_output = Dense(5 * 3, activation='linear', name='colors')(x)

    model = Model(inputs=input_layer, outputs=[aesthetic_output, color_output])

    model.compile(optimizer='adam', 
                  loss={'aesthetic': 'sparse_categorical_crossentropy', 'colors': 'mean_squared_error'},
                  metrics={'aesthetic': 'accuracy', 'colors': 'mae'})  # MAE for color regression

    return model

# Main execution
if __name__ == "__main__":
    dataset_dir = r"D:\Portfolio\HomeDecorApp\automated-home-decor\dataset"  # Path to dataset
    object_detection_model_path = r"D:\Portfolio\HomeDecorApp\automated-home-decor\models\object detection\ssd_mobilenet_v2_320x320_coco17_tpu-8\saved_model"
    object_detection_model = load_object_detection_model(object_detection_model_path)

    # Load the aesthetic model (MobileNetV2)
    aesthetic_model = MobileNetV2(weights='imagenet')

    # Process the images and labels
    X_images, y_aesthetic, y_colors = process_image_folder(dataset_dir, object_detection_model, aesthetic_model)

    # Build and train the model
    model = build_multi_output_model()
    model.fit(X_images, {'aesthetic': y_aesthetic, 'colors': y_colors}, epochs=10, batch_size=32)

    # Save the trained model
    model.save("output/trained_decor_model.h5")

