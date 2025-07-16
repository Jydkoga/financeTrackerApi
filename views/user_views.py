from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.category import Category
from models.user import User
from serializers.user_serializer import BasicUserSchema, FullUserSchema
from flask_cors import cross_origin
from serializers.transaction_group_serializer import transaction_groups_schema
from marshmallow.exceptions import ValidationError

user_bp = Blueprint("user", __name__)

basic_user_schema = BasicUserSchema()
basic_users_schema = BasicUserSchema(many=True)
full_user_schema = FullUserSchema()


@user_bp.route("/", methods=["GET"])
@cross_origin()
def get_all_users():
    try:
        users = User.query.all()
        return jsonify(basic_users_schema.dump(users)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/add", methods=["POST"])
@cross_origin()
def add_user():
    try:
        data = request.get_json()
        print("Received data for new user:", data)
        schema = FullUserSchema(session=db.session)
        print("schema:", schema)
        new_user = schema.load(data)
        print("Loaded new user:", new_user)
        db.session.add(new_user)
        print("Committing user to DB...")
        db.session.commit()
        print("User successfully added with ID:", new_user.id)
        return jsonify(schema.dump(new_user)), 201
    except ValidationError as ve:
        print("ValidationError:", ve.messages)
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        print("Error during commit:", str(e))
        return jsonify({"error": str(e)}), 400


@user_bp.route("/lookup", methods=["GET"])
@cross_origin()
def lookup_user():
    try:
        username = request.args.get("username")
        print(f"Looking up user with username: {username}")
        if not username:
            return jsonify({"error": "Username parameter is required"}), 400

        user = User.query.filter_by(username=username).first()
        print("User from DB:", user)
        return jsonify({"exists": bool(user)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not user.check_password(password):
            return jsonify({"error": "Invalid password"}), 401

        return jsonify(basic_user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/<int:user_id>/transaction_groups", methods=["GET"])
@cross_origin()
def get_user_transaction_groups(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        transaction_groups = user.transaction_groups
        print(f"Transaction groups raw: {transaction_groups}")

        serialized_groups = transaction_groups_schema.dump(transaction_groups)
        print(f"Serialized groups: {serialized_groups}")
        return jsonify(serialized_groups), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
