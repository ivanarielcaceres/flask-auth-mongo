from mongoengine import Document, StringField

class Project(Document):
    name = StringField(max_length=32)
    description= StringField(max_length=100)