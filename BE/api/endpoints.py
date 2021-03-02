import os
import tempfile
from PIL import Image
import face_recognition
import numpy as np
from numpy.core.numeric import NaN
from starlette.responses import JSONResponse
import models
from marshmallow import ValidationError
from json.decoder import JSONDecodeError
import mongoengine
from face.images import resize_and_reorient, ImageException
from face import face_api
from bson import ObjectId, Binary
import pickle
from starlette.exceptions import HTTPException
from io import BytesIO
import re 

#create user encoding
#recognize user from other enodings
#delete user from other encodings

async def create_organization(request):
    body = await request.form()
    organizationSchema = models.OrganizationSchema()
    try:
        data = organizationSchema.load(body)
        if data:
            name: str = data['name']
            email: str = data['email']
            organization = models.Organization()
            organization.name = name
            organization.email = email
            organization = organization.save()
            context = {
                "organization_id": str(organization.id),
                "organization_name": organization.name,
                "organization_email": organization.email,
            }
            return JSONResponse(context, 201)

    except ValidationError as e:
        context = {
            'detail': "ValidationError",
            "errors": e.messages,
        }
        return JSONResponse(context, 400)
        
    except mongoengine.errors.NotUniqueError as e:
        context = {
            'detail': "NotUniqueError",
            "errors": 'Organization Email Exists',
        }
        return JSONResponse(context, 400)

    except JSONDecodeError as e:
        context = {
            'detail': "JSONDecodeError",
            "errors": e.messages,
        }
        return JSONResponse(context, 400)
    return JSONResponse(status_code=400)



async def create_user_encodings(request):
    body = await request.form()
    userSchema = models.MemberSchema()
    try:
        data = userSchema.load(body)
        if data:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            organization = data['organization']
            bytes_image = await body["image_array"].read()
            bytes_image = BytesIO(bytes_image)
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.jpg', delete=True, prefix=os.path.basename(__file__)) as tf:
                temp_image = Image.open(bytes_image)
                temp_image.save(tf, temp_image.format)
                image : Image = resize_and_reorient(tf)
                image_array = np.array(image)
                face_locations : list = face_api.detect_faces(image_array)
            face_encoding = face_api.face_encodings(image_array, face_locations)
            member  = models.Member()
            member.first_name = str(first_name)
            member.last_name = str(last_name)
            member.email = str(email)
            member.organization = ObjectId(organization)
            member.image_array = Binary(pickle.dumps(image_array, protocol=2), subtype=128 )
            member.face_recognized = True
            member = member.save()

            member_encoding = models.MemberEncoding()
            member_encoding.member = member.id
            member_encoding.organization = ObjectId(organization)
            member_encoding.face_encoding = Binary(pickle.dumps(face_encoding[0], protocol=2), subtype=128 )
            member_encoding = member_encoding.save()
            context = {
                "member_id": str(member.id),
                "member_email": member.email,
                "member_first_name": member.first_name,
                "member_last_name": member.last_name,
            }
            return JSONResponse(context, 201)
    except ValidationError as e:
        context = {
            'detail': "ValidationError",
            "errors": e.messages,
        }
        return JSONResponse(context, 400)


    except ImageException as e:
        context = {
            'detail': "ImageException",
            "errors": str(e.messages),
        }
        return JSONResponse(context, 400)

    except face_api.FaceException as e:
        context = {
            'detail': "FaceException",
            'errors': e.messages,
        }
        return JSONResponse(context, 400)


    except mongoengine.errors.NotUniqueError as e:
        context = {
            'detail': "NotUniqueError",
            "errors": 'User email already exists',
        }
        return JSONResponse(context, 400)

    except JSONDecodeError as e:
        context = {
            'detail': "JSONDecodeError",
            "errors": e.messages,
        }
        return JSONResponse(context, 400)
    finally:
        tf.close()
        bytes_image.close()

async def get_organization(request):
    body = await request.form()
    organizationSchema = models.OrganizationSchema()
    try:
        data = organizationSchema.load(body)
        if data:
            email: str = data['email']
            organization = models.Organization.objects().get(email__icontains=email)
            context = {
                "organization_id": str(organization.id),
                "organization_name": organization.name,
                "organization_email": organization.email,
            }
            return JSONResponse(context, 201)

    except models.Organization.DoesNotExist as e:
        context = {
            "detail": "DoesNotExist"
        }
        return JSONResponse(context, 404)
    
    except ValidationError as e:
        context = {
            'detail': "ValidationError",
            "errors": e.messages,
        }
        return JSONResponse(context, 400)

async def recognize_user(request):
    body = await request.form()
    try:
        data = models.MemberEncodingSchema()
        if data:
            organization = body['organization']
            bytes_image = await body["image"].read()
            bytes_image = BytesIO(bytes_image)
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.jpg', delete=True, prefix=os.path.basename(__file__)) as tf:
                temp_image = Image.open(bytes_image)
                temp_image.save(tf, temp_image.format)
                image : Image = resize_and_reorient(tf)
                image_array = np.array(image)
                face_locations : list = face_api.detect_faces(image_array)
            unknown_face_encoding = face_api.face_encodings(image_array, face_locations)
            
            # Get all organization encodings
            organization = models.Organization.objects().get(id=organization)
            members_encodings = [member for member in models.MemberEncoding.objects().filter(organization=organization) ]

            member_face_encodings = []
            member_oids = []
            for member in members_encodings:

                member_oids.append(member.id)
                member_face_encodings.append(pickle.loads(member.face_encoding))
            face_distances = face_recognition.face_distance(member_face_encodings, unknown_face_encoding[0])
            print(face_distances)
            best_match_index = np.argmin(face_distances) # This returns the face with the min face distance match
            # The face with the nearest match index is not necessarily the face with the closest match.
            print(type(int(best_match_index)))
            matches = face_recognition.compare_faces(member_face_encodings, unknown_face_encoding[0], 0.6)
            print(matches)

            #if matches[best_match_index]:
                # Use the compare mechanisim to find out if the face is truly a match
                #matches = face_recognition.compare_faces([member_face_encodings[best_match_index]], unknown_face_encoding)
                #print(matches)


            # Use face distance to loop and check for the most probable match

            # If there is a face with a close distance, use face compare to check if the face actually matches

            # Make the function async and give frontend 
        return JSONResponse(status_code=200)
    except Exception as e:
        raise e


async def delete_user(request):
    pass

async def train_user_model(request):
    pass

async def fetch(request):
    pass


async def add_more_pics(request):
    pass

