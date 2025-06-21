from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.category import Category
from models.user import User
from serializers.user_serializer import user_schema, users_schema
from flask_cors import cross_origin

transaction_bp = Blueprint('user', __name__)

@transaction_bp.route('/,methods=["GET"]')
@cross_origin()
def get_user():
    try:
        user = User.query.all()
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@transaction_bp.route('/add', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        new_user = user_schema.load(data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400