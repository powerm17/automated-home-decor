import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans
from classMapping import CLASS_ID_TO_NAME  # Import the mapping

# Use your downloaded model path here
model_path = r"D:\Portfolio\HomeDecorApp\automated-home-decor\models\object detection\ssd_mobilenet_v2_320x320_coco17_tpu-8\saved_model"
model = tf.saved_model.load(model_path)

# Example product catalog (replace this with actual data from your database or API)
product_catalog = [
    {"name": "Modern Sofa", "category": "sofa", "price": 499, "image": "sofa_image_url"},
    {"name": "Stylish Lamp", "category": "lamp", "price": 59, "image": "lamp_image_url"},
    {"name": "Wooden Dining Table", "category": "dining table", "price": 349, "image": "table_image_url"},
    {"name": "Elegant Chair", "category": "chair", "price": 129, "image": "chair_image_url"},
    # TODO: Integrate API for real data
]

# Load and preprocess image
def load_image(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")  # Ensure image is in RGB mode
    image_np = np.array(image)
    return image_np

# Run detection on an image
def detect_objects(image_np):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]  # Add batch dimension
    detections = model(input_tensor)
    return detections

# Extract bounding boxes and class IDs
def extract_detections(detections):
    boxes = detections['detection_boxes'][0].numpy()
    class_ids = detections['detection_classes'][0].numpy()
    return boxes, class_ids

# Detect furniture in the image
def detect_furniture_in_image(image_path):
    image_np = load_image(image_path)
    detections = detect_objects(image_np)
    boxes, class_ids = extract_detections(detections)
    
    detected_items = []
    num_detections = int(detections['num_detections'][0].numpy())
    
    # Print the class ids and names for debugging
    for i in range(num_detections):
        class_id = int(detections['detection_classes'][0][i].numpy())
        score = detections['detection_scores'][0][i].numpy()
        
        if score > 0.5:  # Only consider detections with a high score
            class_name = CLASS_ID_TO_NAME.get(class_id, 'Unknown')
            print(f"Detected class ID: {class_id}, Name: {class_name}, Score: {score}")  # Debug line
            detected_items.append(class_name)

    return detected_items

# Extract the prominent colors from the image using k-means clustering
def extract_colors_from_image(image_path, num_colors=3):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image = image.reshape((image.shape[0] * image.shape[1], 3))  # Reshape the image into a list of pixels

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(image)
    colors = kmeans.cluster_centers_.astype(int)

    # Convert colors into hex format for easier readability
    hex_colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in colors]
    return hex_colors

def get_suggestions(detected_items, product_catalog):
    """Suggest products based on detected objects."""
    suggestions = []
    for detected_item in detected_items:
        for product in product_catalog:
            # Match detected object with product categories
            if detected_item.lower() in product['category'].lower():
                suggestions.append(product)
    
    return suggestions

def process_uploaded_image(image_path):
    # Detect objects in the uploaded image
    detected_items = detect_furniture_in_image(image_path)
    
    # Get product suggestions based on detected objects
    suggestions = get_suggestions(detected_items, product_catalog)
    
    return suggestions

# Test with a sample image
image_path = r"D:\Portfolio\HomeDecorApp\automated-home-decor\dataset\boho\image1.jpg"
detected_items = detect_furniture_in_image(image_path)
prominent_colors = extract_colors_from_image(image_path)

# Print detected items and prominent colors
print("Detected Items:", detected_items)
print("Prominent Colors:", prominent_colors)

# Print out suggested items based on detection
suggested_items = process_uploaded_image(image_path)
for item in suggested_items:
    print(f"Suggested: {item['name']} - Price: ${item['price']}")
    print(f"Image URL: {item['image']}")
