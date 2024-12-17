import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

def load_deeplab_model(model_path):
    """Load the pre-trained DeepLabV3+ model."""
    return load_model(model_path)

def segment_image(model, image):
    """Perform segmentation on the image using the loaded model."""
    image_resized = cv2.resize(image, (512, 512))
    input_image = np.expand_dims(image_resized / 255.0, axis=0)
    mask = model.predict(input_image)[0]
    mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
    return (mask_resized > 0.5).astype(np.uint8)

def detect_face(image):
    """Detect faces in the image using OpenCV's Haar cascades."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def crop_to_face(image, faces):
    """Crop the image to the region containing the face."""
    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    # Use the first detected face (can be adjusted for multiple faces)
    x, y, w, h = faces[0]
    return image[y:y + h, x:x + w]

def create_passport_photo(model_path, input_image_path, output_image_path):
    """Generate a passport-size photo with background removed."""
    # Load the model
    model = load_deeplab_model(model_path)

    # Load the input image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError(f"Could not read image from {input_image_path}")
# sreem 
    # Detect faces
    faces = detect_face(image)

    # Crop to the first detected face
    cropped_image = crop_to_face(image, faces)

    # Perform background removal
    mask = segment_image(model, cropped_image)
    segmented_image = cv2.bitwise_and(cropped_image, cropped_image, mask=mask)

    # Resize to passport dimensions (e.g., 413x531 pixels)
    passport_size = (413, 531)
    resized_image = cv2.resize(segmented_image, passport_size)

    # Save the output
    cv2.imwrite(output_image_path, resized_image)

# Example usage
# Assuming 'deeplab_model.h5' is the trained model file in the current directory
# and 'input.jpg' is the input image to process.
# create_passport_photo('deeplab_model.h5', 'input.jpg', 'output.jpg')
