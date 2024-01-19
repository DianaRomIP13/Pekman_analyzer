import numpy as np
from keras.models import load_model

def predict_fake_smile(img_array):
    model = load_model("/Users/dianarom/Desktop/Pekman_analyzer/models/smile_fake_real_model.h5")
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])

    class_names = {0: 'fake smile', 1: 'real smile'}
    class_name = class_names[predicted_class_index]

    return class_name

