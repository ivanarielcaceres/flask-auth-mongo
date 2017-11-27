import tempfile
from app.model.project import Project
from app.model.user import User
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask import abort, request, jsonify, g

app = Flask(__name__)
app.config.from_object('app.config.DevelopmentConfig')
auth = HTTPBasicAuth()
db = MongoEngine(app)

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        try:
            user = User.objects.get(username=username_or_token)
            if check_password_hash(user.password_hash, password) is True:
                user['id'] = str(user['id'])
                g.user = user
                return g.user
            else:
                return False
        except User.DoesNotExist:
            return False

    g.user = user
    return True

@app.route('/api/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    fullname = request.json.get('fullname')
    if username is None or password is None or fullname is None:
        abort(400)
    try:
        User.objects.get(username=username)
        abort(400)
    except User.DoesNotExist:
        user = User(username=username, fullname=fullname)
        user.hash_password(password)
        user.save()
    return jsonify({'username': user.username, 'fullname': user.fullname})

@app.route('/api/login', methods=['GET'])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@app.route('/api/users', methods=['GET'])
@auth.login_required
def get_user_info():
    user = g.user
    return jsonify({'username': user.username,  'fullname': user.fullname})

@app.route('/api/projects', methods=['GET'])
@auth.login_required
def get_projects():
    author = g.user
    projects = Project.objects(author=author)
    return jsonify({'projects': projects})

@app.route('/api/projects', methods=['POST'])
@auth.login_required
def create_project():
    name = request.json.get('name')
    description = request.json.get('description')
    author = g.user
    
    image = request.json.get('image')
    image_decoded = base64.b64decode(image)
    image_bytes = bytearray(image_decoded)    
    if name is None or description is None:
        abort(400)

    project = Project(name=name, description=description, author = author)
    save_image(image_bytes, project)
    project.save()
    return jsonify({'name': project.name, 'description': project.description})

def save_image(image_bytes):
    with tempfile.TemporaryFile() as f:
        f.write(image_bytes)
        f.flush()
        f.seek(0)
        project.image.put(f)