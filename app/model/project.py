from mongoengine import Document, StringField, ReferenceField, ListField
from app.model.user import User

class Project(Document):
    name = StringField(max_length=32)
    description= StringField(max_length=100)
    author = ReferenceField(User)
    files_path = ListField(StringField())
