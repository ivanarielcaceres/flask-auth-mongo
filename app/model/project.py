from mongoengine import Document, StringField, ReferenceField
from app.model.user import User

class Project(Document):
    name = StringField(max_length=32)
    description= StringField(max_length=100)
    author = ReferenceField(User)