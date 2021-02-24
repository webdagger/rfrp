import os
from typing import List

import face_recognition
import numpy as np
from exceptions import FaceRecognitionExeption, ImageManipulationError
from image_manipulation import oriented_thumbnail
from PIL import Image


def face_locations(image_path: str, number_of_times_to_upsample=1, model="hog"):
    """

    face_locations first manipulates the given image, before looking for the face.

    """
    try:
        print(
            "***************************************************************************************"
        )
        print("Detecting Face Location")
        print(
            "***************************************************************************************"
        )
        directory = os.path.dirname(image_path)
        im = Image.open(image_path)
        im = oriented_thumbnail(im)
        print(
            "***************************************************************************************"
        )
        print("Created Unknown Face thumbnail")
        print(
            "***************************************************************************************"
        )
        print(
            "***************************************************************************************"
        )
        print("Starting Face locations")
        print(
            "***************************************************************************************"
        )
        image = np.array(im)
        face_locations = face_recognition.face_locations(
            image, number_of_times_to_upsample, model
        )
        if len(face_locations) < 1:
            raise FaceRecognitionExeption("Could not get face locations")
        return face_locations
    
    except FaceRecognitionExeption as e:
        print(e)
        raise FaceRecognitionExeption("Error manipulating image in face_locations.py")  

    except ImageManipulationError as e:
        print(e.args)
        raise ImageManipulationError("Error manipulating image in face_locations.py")
    
    except Exception as e:
        print(e)
        raise e
