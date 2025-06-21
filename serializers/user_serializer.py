from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    total_balance = fields.Float(required=True)
    transactions = fields.List(fields.Nested('TransactionSchema', exclude=('user',)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)