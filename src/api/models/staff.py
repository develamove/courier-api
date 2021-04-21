from src.extensions import bcrypt, database, marshmallow
from sqlalchemy import Column, DateTime, Integer, String, func
from marshmallow import fields


class StaffModel(database.Model):
    __tablename__ = 't_staff'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(100))
    role = Column(String(20))
    set_timestamp = Column(DateTime, nullable=True)
    registered_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, username, password, role):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.role = role

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

    def __repr__(self):
        return '<Staff %r>' % self.username


class StaffSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = StaffModel
        strict = True

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)
    type = fields.Str(missing='')
    set_timestamp = fields.DateTime(dump_only=True)
    registered_timestamp = fields.DateTime(dump_only=True)

