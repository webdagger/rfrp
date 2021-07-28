import os
import pickle
import sys
import tempfile
from exceptions import ImageManipulationError, FaceRecognitionExeption
import face_encodings
import face_locations
import face_recognition
import numpy as np
from image_manipulation import oriented_thumbnail
from PIL import Image


# Load face encodings
try:

    with open("dataset_faces.dat", "rb") as f:
        all_face_encodings = pickle.load(f)
except FileNotFoundError:
    all_face_encodings = {}

# Grab the list of names and the list of encodings
names = list(all_face_encodings.keys())
encodings = np.array(list(all_face_encodings.values()))

all_unknown_images = []
directory = "unknown/"
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.lower().endswith(".jpg".lower()):
            all_unknown_images.append(os.path.join(root, file))
for image in all_unknown_images:
    try:
        im = oriented_thumbnail(Image.open(image))
        with tempfile.NamedTemporaryFile(mode="wb", suffix='.jpg', delete=True, prefix=os.path.basename(__file__)) as tf:
            im.save(tf, im.format)
            unknown_face_locations = face_locations.face_locations(tf.name, number_of_times_to_upsample=2, model="hog")
            print(tf.name)
            unknown_face = face_encodings.FaceEncodings(
                tf.name, known_face_locations=unknown_face_locations
            ).get_encodings()
            result = face_recognition.compare_faces(encodings, unknown_face)
            print(result)
            names_with_result = list(zip(names, result))

    
    except ImageManipulationError as e:
        print(e)
        print(image)
        print('odood')
        pass

    except FaceRecognitionExeption as e:
        print(e)
        print(image)
        print('ljdjdjdj')
        pass


    except Exception as e:
        print(image)
        print(e)
        #sys.exit(0)
        pass
    finally:
        tf.close()
# Print the result as a list of names with True/False
print(names_with_result)