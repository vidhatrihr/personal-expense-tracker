from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  name, email, password = data['name'], data['email'], data['password']

  if User.query.filter_by(email=email).first():
    return jsonify({'message': 'Email already registered'}), 400

  user = User(name=name, email=email, password=generate_password_hash(password))
  db.session.add(user)
  db.session.commit()

  login_user(user)
  return jsonify({'message': 'Registered successfully'})


@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email, password = data['email'], data['password']

  user = User.query.filter_by(email=email).first()

  if not user or not check_password_hash(user.password, password):
    return jsonify({'message': 'Invalid credentials'}), 401

  login_user(user)
  return jsonify({'message': 'Logged in', 'data': {'name': user.name, 'email': user.email}})


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logged out'})


@auth_bp.route('/whoami', methods=['GET'])
@login_required
def whoami():
  return jsonify({'data': {'name': current_user.name, 'email': current_user.email}})
