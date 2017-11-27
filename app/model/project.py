from mongoengine import Document, StringField, ReferenceField, ImageField
from app.model.user import User

class Project(Document):
    name = StringField(max_length=32)
    description= StringField(max_length=100)
    author = ReferenceField(User)
    image = ImageField()