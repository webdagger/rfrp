import face_encodings
import face_locations
import face_recognition
import numpy as np
from exceptions import FaceRecognitionExeption, ImageManipulationError


def face_comparism(image: str, known_face_encodings, known_face_names):
    """
    Face gets the face encoding of a given image and compares it with the known faces encodings
    """
    try:
        face_location = face_locations.face_locations(
            image, number_of_times_to_upsample=2
        )
        unknown_face_encodings = face_encodings.FaceEncodings(
            image, known_face_locations=face_location, num_jitters=20, model="large"
        )
        if len(unknown_face_encodings) < 1:
            raise FaceRecognitionExeption(
                "Could not detect any face from the picture given"
            )

        for face_encoding in unknown_face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            name = "No Match"
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                return name
        return name

    except (FaceRecognitionExeption, ImageManipulationError, Exception) as e:
        raise e
