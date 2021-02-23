import face_recognition
import os
from typing import List
from face_recognition.api import face_distance
import numpy as np

""" user_one = face_recognition.load_image_file('./database/fish/01.jpg')
user_one_encoding = face_recognition.face_encodings(user_one)[0]

user_two = face_recognition.load_image_file('./database/fray/02.jpg')
user_two_encoding = face_recognition.face_encodings(user_two)[0]

known_face_encodings = [
    user_one_encoding,
    user_two_encoding
]

"""



# Walk in the folder to add every file name to known_faces_filenames
directory = 'database/'
filetype = '.jpg'

def known_faces(directory : str) -> List[list]:
    """
    known_faces takes a filepath containing the database for the jpg images and returns a list
        containing 2 items
            1 the known_face_encodings
             2 the known_face_names 
    """
    # get the directory name
    # get only the first image in the directory, get its encoding known_face_encodings
    # save the directory name as the known_face_name
    known_face_encodings : List = []
    known_face_names : List = []
    paths : List = []
    
    # Walk the directory.
    for root, dirs, files in os.walk(directory):
        # Save the directory name as the known_face_name
        for dir in dirs:
            known_face_names.append(dir)
        
        for file in files:
            # This adds only the 01.jpg picture to the list.
            if file.lower().endswith('01.jpg'.lower()):
                paths.append(os.path.join(root, file))
            
    
    # Create the image file encoding
    for path in paths:
        face = face_recognition.load_image_file(path)
        known_face_encodings.append(face_recognition.face_encodings(face)[0])

    return (known_face_encodings, known_face_names)
try:
    known_face_encodings, known_face_names = (known_faces(directory))
    print(f'We have {len(known_face_encodings)} face encodings')
    print(f'We have {len(known_face_names)} names')
except Exception as e:
    print(e)
    exit(1)
# Dectect face. 
unknown : str = 'unknown/03.jpg'

try:
    print('s')
    unknown_picture = face_recognition.load_image_file(unknown)
    print('o')
except Exception as e:
    print('Could not load image')
    print(e)
    exit(1)


try:
    print('a')
    unknown_face_locations = face_recognition.face_locations(unknown_picture)
    print(unknown_face_locations)

except Exception as e:
    print('Could not detect face')
    print(e)
    exit(1)

try:
    print('r')
    unknown_face_encodings = face_recognition.face_encodings(unknown_picture, unknown_face_locations)
    print(unknown_face_encodings)
except Exception as e:
    print('Could not detect face encodings')
    print(e)
    exit(1)
try:
    print('sd')
    for face_encoding in unknown_face_encodings:
        #print(face_encoding)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if matches:
            print(f'We have {len(matches)} matches')
        else:
            print('matches returned 0')
            raise ValueError
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        print(name)

except (Exception, ValueError) as e:
    print(e)
print('xoxoxox')

""" 
def list_files(filepath, filetype):
   paths = []
   for root, dirs, files in os.walk(filepath):
      for file in files:
        
         if file.lower().endswith(filetype.lower()):
            paths.append(os.path.join(root, file))
   return(paths)

c = list_files(filepath, filetype)

print(c)
 """