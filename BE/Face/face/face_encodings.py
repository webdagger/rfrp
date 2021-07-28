from typing import List

import face_recognition
from exceptions import FaceRecognitionExeption


class FaceEncodings:
    """
    Class takes a single image and uses the face_recognition class to get the face encoding.
    """

    def __init__(
        self, image: str, known_face_locations=None, num_jitters=1, model="small"
    ):
        """
        :params image: Path of image file to get face encoding from
        :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
        :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
        :param model: Optional - which model to use. "large" (default) or "small" which only returns 5 points but is faster.
        :return: A list of 128-dimensional face encodings (one for each face in the image)
        """
        self._image = face_recognition.load_image_file(image)
        if known_face_locations is None:
            self._known_face_locations = face_recognition.face_locations(
                self._image, number_of_times_to_upsample=2
            )
        else:
            self._known_face_locations = known_face_locations
        self._num_jitters: int = num_jitters
        self._model: str = model

    def get_encodings(self) -> List:
        encodings: List = face_recognition.face_encodings(
            self._image, self._known_face_locations, self._num_jitters, self._model
        )
        if len(encodings) < 1:
            raise FaceRecognitionExeption(
                "Could not get face encodings from given image file"
            )
        return encodings
