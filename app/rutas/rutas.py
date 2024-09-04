from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, render_template
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['POST'])
def register():
    return jsonify({"msg": "User created successfully"}), 201


@main_bp.route('/')
def index():
    current_time = datetime.now()
    return render_template('index.html', current_time=current_time)

'''
@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401

@main_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
'''