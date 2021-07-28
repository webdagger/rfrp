import pickle

from known_faces import known_faces

# Walk in the folder to add every file name to known_faces_filenames
directory = "database/"

print(
    "***************************************************************************************"
)
print("Creating dataset file")
print(
    "***************************************************************************************"
)
try:
    all_face_encodings = known_faces(directory)
    with open("dataset_faces.dat", "wb") as f:
        pickle.dump(all_face_encodings, f)
    f.close()
except Exception as e:
    raise e

print(
    "***************************************************************************************"
)
print("Finished dataset file")
print(
    "***************************************************************************************"
)
