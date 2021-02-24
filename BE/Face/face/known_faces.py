import os
import sys
from typing import Any, Dict, List

import face_encodings
from exceptions import FaceRecognitionExeption, ImageManipulationError
from image_manipulation import ImageManipulation


def known_faces(directory: str) -> Dict[str, Any]:
    """
    known_faces takes a filepath containing the database for the jpg images and returns a dict
    containing the {known_face_names, known_face_encodings}.
    """

    # Manipulate all the images in the directory
    print(
        "***************************************************************************************"
    )
    print(f"Starting {directory} Image Manipulation")
    print(
        "***************************************************************************************"
    )
    try:
        ImageManipulation(directory).manipulate()
    except (ImageManipulationError, Exception) as e:
        print("Fatal error, Could not manipulate images")
        print("***Error***")
        print(e)
        print("Exiting")
        sys.exit(1)

    print(f"Finished {directory} Image Manipulation")
    print(
        "***************************************************************************************"
    )
    known_face_encodings: List = []
    known_face_names: List = []
    paths: List = []

    print(
        "***************************************************************************************"
    )
    print("Walking the Directory")
    print(
        "***************************************************************************************"
    )

    # Walk the directory.
    for root, dirs, files in os.walk(directory):
        # Save the directory name as the known_face_name
        for dir in dirs:
            known_face_names.append(dir)

        for file in files:
            # This adds only the 01.jpg picture to the list.
            if file.lower().endswith("01.thumbnail.jpg".lower()):
                paths.append(os.path.join(root, file))

    print(
        "***************************************************************************************"
    )
    print("Creating Face Encodings")
    print(
        "***************************************************************************************"
    )
    # Create the image file encoding
    for path in paths:
        try:
            face_encoding = face_encodings.FaceEncodings(
                path, num_jitters=100, model="large"
            )
            known_face_encodings.append(face_encoding.get_encodings()[0])
        except (FaceRecognitionExeption, Exception) as e:
            print("***Error***")
            print(f"Error, Could not get face encodings for {path}")
            print(e)
            # Remove the offending name from the known_face_names
            # This allows us to prevent messing up the len(known_face_names)
            offending_directory: str = os.path.basename(os.path.dirname(path))
            if offending_directory in known_face_names:
                known_face_names.remove(offending_directory)

    zip_iterator = zip(known_face_names, known_face_encodings)
    print(
        "***************************************************************************************"
    )
    print("Finished Creating Face Encodings")
    print(
        "***************************************************************************************"
    )
    return dict(zip_iterator)
