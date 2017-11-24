from mongoengine import Document, StringField
from werkzeug.security import generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
                          
class User(Document):
    username = StringField(max_length=32)
    fullname = StringField(max_length=100)
    password_hash = StringField()

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def generate_auth_token(self, expiration=600):
        s = Serializer('sdafdkjhsfmcvbbasjjsafghghgsd\sa', expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('sdafdkjhsfmcvbbasjjsafghghgsd\sa')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = User.objects.get(id=bson.objectid.ObjectId(data['id']))
        return user