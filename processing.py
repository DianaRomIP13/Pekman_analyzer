from face_detection import preprocess_image
from class_emotion import predict_emotion
from predict_fake_smile import predict_fake_smile
from predict_fake_sad import predict_fake_sad
from predict_fake_fear import predict_fake_fear
from video_classifier import classify_video


def processing_file(new_path):
    result = None  # Initialize result variable

    file_type = new_path.split('.')[-1].lower()
    if file_type in ['jpg', 'jpeg', 'png', 'gif']:
        print(f"Processing image: {new_path}")
        img_path = new_path
        processed_image = preprocess_image(img_path)
        predicted_class = predict_emotion(processed_image)
        print(f"Predicted class: {predicted_class}")

        if predicted_class.lower() == "sad":
            predicted_class = predict_fake_sad(processed_image)
            print(f"Predicted class: {predicted_class}")
        elif predicted_class.lower() == "happy":
            predicted_class = predict_fake_smile(processed_image)
            print(f"Predicted class: {predicted_class}")
        elif predicted_class.lower() == "fear":
            predicted_class = predict_fake_fear(processed_image)
            print(f"Predicted class: {predicted_class}")
        result = predicted_class
    elif file_type in ['mp4', 'avi', 'mov']:
        print(f"Processing video: {new_path}")
        processed_frames = classify_video(new_path, show_video=False)
        result = processed_frames
    else:
        print(f"Unsupported file type: {file_type}")

    return result