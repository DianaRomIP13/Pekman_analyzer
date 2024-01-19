import cv2
import dlib
import numpy as np
from keras.models import load_model

def classify_emotion(frame, model, emotion_dict):
    emotion_result = model.predict(frame)

    predicted_class = np.argmax(emotion_result)

    emotion_label = emotion_dict.get(predicted_class)

    return emotion_label

def classify_video(video_path, show_video=True):
    emotion_model = load_model("/Users/dianarom/Desktop/Pekman_analyzer/models/emotions_class_model.h5")
    happy_model = load_model('/Users/dianarom/Desktop/Pekman_analyzer/models/smile_fake_real_model.h5')
    sad_model = load_model('/Users/dianarom/Desktop/Pekman_analyzer/models/sad_fake_real_model.h5')
    fear_model = load_model('/Users/dianarom/Desktop/Pekman_analyzer/models/smile_fake_real_model.h5')

    emotions_dict = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
    happy_dict = {0: 'fake smile', 1: 'real smile'}
    sad_dict = {0: 'fake sadness', 1: 'real sadness'}
    fear_dict = {0: 'fake fear', 1: 'real fear'}

    # Initializing the face detector dlib
    detector = dlib.get_frontal_face_detector()

    # Launching a video stream
    vs = cv2.VideoCapture(video_path)

    # Variable for storing processed frames
    processed_frames = []

    # Displaying and processing frames
    while True:
        ret, frame = vs.read()

        # Check if the frame is empty
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (48, 48))
            face_roi = np.reshape(face_roi, [1, 48, 48, 1])

            result = emotion_model.predict(face_roi)
            emotion_label = np.argmax(result)
            emotion_prediction = emotions_dict[emotion_label]

            if emotion_label == 3:
                result_label = classify_emotion(face_roi, happy_model, happy_dict)
            elif emotion_label == 5:
                result_label = classify_emotion(face_roi, sad_model, sad_dict)
            elif emotion_label == 2:
                result_label = classify_emotion(face_roi, fear_model, fear_dict)
            else:
                result_label = ''

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"{emotion_prediction} ({result_label})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Adding the processed frame to a variable
        processed_frames.append(frame)

        # Displaying a frame if the show_video parameter is set
        if show_video:
            cv2.imshow("Emotion Recognition", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vs.release()
    cv2.destroyAllWindows()

    return processed_frames


