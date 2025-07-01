from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.user import User
from marshmallow_sqlalchemy.fields import Nested
from serializers.transaction_serializer import TransactionSchema  
from serializers.transaction_group_serializer import TransactionGroupSchema 


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
        load_instance = True

    id = auto_field()
    username = auto_field()
    total_balance = auto_field()
    transactions = Nested(TransactionSchema, many=True)
    transaction_groups = Nested(TransactionGroupSchema, many=True)
   

basic_user_schema = BasicUserSchema()
full_user_schema = FullUserSchema()