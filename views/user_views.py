from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.category import Category
from models.user import User
from serializers.user_serializer import user_schema, users_schema, UserSchema
from flask_cors import cross_origin

user_bp = Blueprint('user', __name__)

@user_bp.route('/',methods=["GET"])
@cross_origin()
def get_all_users():
    try:
        user = User.query.all()
        return jsonify(users_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@user_bp.route('/add', methods=['POST'])
@cross_origin()
def add_user():
    try:
        data = request.get_json()
        schema = UserSchema(session=db.session)
        new_user = schema.load(data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(schema.dump(new_user)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@user_bp.route('/lookup', methods=['GET'])
@cross_origin()
def lookup_user():
    try:
        username = request.args.get('username')
        print(f"Looking up user with username: {username}")
        if not username:
            return jsonify({"error": "Username parameter is required"}), 400
        
        user = User.query.filter_by(username=username).first()
        print("User from DB:", user)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
