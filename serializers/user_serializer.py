from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.user import User
from marshmallow_sqlalchemy.fields import Nested
from serializers.transaction_serializer import TransactionSchema  # adjust path as needed



class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    total_balance = auto_field(required=True)
    transactions = Nested(TransactionSchema, many=True)
   

user_schema = UserSchema()
users_schema = UserSchema(many=True)