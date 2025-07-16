from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.user import User
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, post_load
from serializers.transaction_serializer import TransactionSchema
from serializers.transaction_group_serializer import TransactionGroupSchema
from werkzeug.security import generate_password_hash


class BasicUserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    total_balance = auto_field(required=True)


class FullUserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    username = auto_field()
    password = fields.Str(load_only=True, required=True)
    total_balance = auto_field()
    transactions = Nested(TransactionSchema, many=True)
    transaction_groups = Nested(TransactionGroupSchema, many=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(
            username=data["username"],
            total_balance=data.get("total_balance", 0.0),
            password=data["password"],
        )


basic_user_schema = BasicUserSchema()
full_user_schema = FullUserSchema()
