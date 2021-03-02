from PIL import Image
import face_recognition
from marshmallow.fields import List
import numpy as np


class FaceException(Exception):
    def __init__(self, messages: str) -> None:
        self.messages = messages



def detect_faces(image: np.array, allow_multiple_faces: bool = False, engine: str = 'face_recognition') -> List:
    """

    Given an Image, use an engine to detect if faces a present in the image
    :params image: A valid pillow image.open(file)
    :params allow_multiple_faces: A boolean to allow multiple pass the check
    :params: engine: A string value that allows the facial recognition api to be 
        independent of the api eg: 'face_recognition' uses https://github.com/ageitgey/face_recognition
    
    :returns: A list containing all [face locations found]
    """

    if engine.lower() == 'face_recognition':
        face_locations: list = face_recognition.face_locations(image)
        number_of_faces_detected: int = len(face_locations)

        if number_of_faces_detected < 1:
            raise FaceException('No face detected. Check lightning and other conditions of image.')

        if number_of_faces_detected > 1 and allow_multiple_faces is False:
            raise FaceException('Multiple Faces Detected, Administrator does not allow this.')
        return face_locations
    else:
        raise FaceException('Invalid engine passed.')


def face_encodings(image_array: np.array, face_locations: tuple = None, engine: str = 'face_recognition') -> list:
    """

    Given an np.array(PIL Image), use an engine to detect if faces a present in the image
    :params image: A valid pillow image.open(file)
    :params: Tuple containg the face locations,  defaults to None
    :params allow_multiple_faces: A boolean to allow multiple pass the check
    :params: engine: A string value that allows the facial recognition api to be 
        independent of the api eg: 'face_recognition' uses https://github.com/ageitgey/face_recognition
    
    :returns: A list containing all face locations found
    """
    if engine.lower() == 'face_recognition':
        if face_locations is None:
            encodings = face_recognition.face_encodings(image_array)
        else:
            encodings = face_recognition.face_encodings(image_array, known_face_locations=face_locations)

        if len(encodings) < 0:
            raise FaceException('Face encoding failed, assert a human face is in the image.')
        return encodings  
    else:
        raise FaceException('Invalid engine passed.')


def distance(known_encodings, unknown_encodings):
    return face_recognition.face_distance(known_encodings, unknown_encodings)