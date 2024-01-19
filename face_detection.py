import cv2
import numpy as np
from mtcnn import MTCNN
from PIL import Image

def preprocess_image(image_path):

    img = Image.open(image_path)

    cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    detector = MTCNN()

    faces = detector.detect_faces(cv_image)

    if faces:
        x, y, w, h = faces[0]['box']
        face_roi = cv_image[y:y + h, x:x + w]

        face_img = Image.fromarray(cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB))

        face_img = face_img.resize((48, 48))
        face_img = face_img.convert('L')
        face_array = np.array(face_img) / 255.0

        face_array = np.expand_dims(face_array, axis=0)
        face_array = np.expand_dims(face_array, axis=-1)

        return face_array
    else:
        print("Face not found")


