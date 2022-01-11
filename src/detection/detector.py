"""
detector = Detector('Haar Cascade') # intialize detector

for img in imgs:
    detector.detect(img) # detect faces in image
"""

import os

import cv2
import mediapipe as mp

# from mtcnn import MTCNN


get_key_point = mp.solutions.face_detection.get_key_point
keys = mp.solutions.face_detection.FaceKeyPoint


class Detectors:
    def __init__(self):
        self.models = {
            "Haar Cascade": HaarCascadeDetector(),
            "Mediapipe": MediapipeFaceDetector(),
            # "MTCNN": MTCNNDetector()
        }

    def loadModel(self, model: str):
        return self.models[model]


class HaarCascadeDetector:
    def __init__(self):
        HAAR_CASCADES_PATH = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "./HaarCascadeDetector/cascades",
        )
        self.detectorPaths = {
            "face": "haarcascade_frontalface_default.xml",
            "eyes": "haarcascade_eye.xml",
            "smile": "haarcascade_smile.xml",
        }
        self.detectors = {}

        for (name, filename) in self.detectorPaths.items():
            self.detectors[name] = cv2.CascadeClassifier(
                os.path.join(HAAR_CASCADES_PATH, filename)
            )

    def detect(self, image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        return self.detectors["face"].detectMultiScale(
            image=gray,
            scaleFactor=scaleFactor,
            minNeighbors=minNeighbors,
            minSize=minSize,
            flags=cv2.CASCADE_SCALE_IMAGE,
        )


class MediapipeFaceDetector:
    def __init__(self):
        self.face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )

    def detect(self, image):
        results = self.face_detection.process(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        )

        if results.detections is None:
            return []

        bboxes = []
        landmarks = []
        height, width, _ = image.shape
        for detection in results.detections:
            bboxes.append(
                [
                    round(
                        detection.location_data.relative_bounding_box.xmin
                        * width
                    ),
                    round(
                        detection.location_data.relative_bounding_box.ymin
                        * height
                    ),
                    round(
                        detection.location_data.relative_bounding_box.width
                        * width
                    ),
                    round(
                        detection.location_data.relative_bounding_box.height
                        * height
                    ),
                ]
            )
            landmarks.append(
                {
                    "LEFT_EYE": 
                    [
                        round(
                            get_key_point(detection, keys.LEFT_EYE).x * width
                        ),
                        round(
                            get_key_point(detection, keys.LEFT_EYE).y * height
                        )
                    ],
                     "RIGHT_EYE": 
                    [
                        round(
                            get_key_point(detection, keys.RIGHT_EYE).x * width
                        ),
                        round(
                            get_key_point(detection, keys.RIGHT_EYE).y * height
                        )
                    ],
                     "NOSE_TIP": 
                    [
                        round(
                            get_key_point(detection, keys.NOSE_TIP).x * width
                        ),
                        round(
                            get_key_point(detection, keys.NOSE_TIP).y * height
                        )
                    ],
                }
            )
        return zip(bboxes, landmarks)


# class MTCNNDetector:
#     def __init__(self):
#         self.detector = MTCNN()

#     def detect(self, image):
#         results = self.detector.detect_faces(
#             cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         )

#         if len(results) == 0: return []

#         return [result["box"] for result in results]