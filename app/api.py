import base64
from app.model.project import Project
from app.model.user import User
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask import abort, request, jsonify, g

UPLOAD_FOLDER='/root/pictures/'
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
    
    images = request.json.get('images')
    project = Project(name=name, description=description, author = author)
    save_images(images, project)
    project.save()
    return jsonify({'name': project.name, 'description': project.description})

def save_images(images, project):
    count = 0
    for image in images:
        file_name = UPLOAD_FOLDER + project.name +  str(count) +'.png'
        count += 1
        image_decoded = base64.b64decode(image)
        image_bytes = bytearray(image_decoded)
        with open(file_name, 'wb') as f:
            f.write(image_bytes)
            project.files_path.append(file_name)
