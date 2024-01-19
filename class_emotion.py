import numpy as np
from keras.models import load_model

def predict_emotion(image):
    model = load_model("/Users/dianarom/Desktop/Pekman_analyzer/models/emotions_class_model.h5", compile=False)
    predictions = model.predict(image)
    predicted_class_index = np.argmax(predictions[0])

    class_names = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
    class_name = class_names[predicted_class_index]

    return class_name


