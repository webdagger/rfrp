from marshmallow import Schema,  fields, ValidationError, validate
import bson
import mongoengine as me
import datetime

from mongoengine.queryset.base import BaseQuerySet


class ObjectId(fields.Field):
    """
    Marshmallow field for :class:`bson.ObjectId`
    """
    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            valid = bson.ObjectId.is_valid(value)
            if valid:
                return bson.ObjectId(value)
        except (TypeError, bson.errors.InvalidId):
            raise ValidationError('Invalid ObjectId.')


class OrganizationSchema(Schema):
    id = ObjectId(dump_only=True) # Make _id field readonly 
    name = fields.Str(validate=validate.Length(min=2, max=255))
    email = fields.Email(required=True, validate=validate.Email())
    allow_multiple_faces = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)


class MemberSchema(Schema):
    id = ObjectId(dump_only=True) # Make _id field readonly
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    email = fields.Email(requred=True, validate=validate.Email())
    organization = ObjectId(required=True)
    image_array = fields.Raw() # We need to store the image in the case we want to change the machine learning model.
    face_recognized = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)


class MemberEncodingSchema(Schema):
    id = ObjectId(dump_only=True) # Make _id field readonly 
    member  = ObjectId(required=True)
    organization = ObjectId(required=True)
    created_at = fields.DateTime(dump_only=True)
    face_encoding = fields.Raw(required=True)
    

class Organization(me.Document):
    name = me.StringField(required= True, max_length=255)
    email = me.EmailField(required= True, unique=True)
    allow_multiple_faces = me.BooleanField(default=False)
    created_at = me.DateTimeField(default=datetime.datetime.now())

    meta = {'allow_inheritance': True}


class Member(me.Document):
    first_name = me.StringField(required= True, max_length=255)
    last_name = me.StringField(required= True, max_length=255)
    email = me.EmailField(required= True, unique=True)
    organization = me.LazyReferenceField(Organization, reverse_delete_rule=me.CASCADE)
    image_array = me.BinaryField()
    face_recognized = me.BooleanField(default=False)
    created_at = me.DateTimeField(default=datetime.datetime.now())
    meta = {'allow_inheritance': True}


class MemberEncoding(me.Document):
    member = me.ReferenceField(Member)
    organization = me.ReferenceField(Organization,  reverse_delete_rule=me.CASCADE)
    created_at = me.DateTimeField(default=datetime.datetime.now())
    face_encoding = me.BinaryField()


    meta = { 'allow_inheritance': True}
