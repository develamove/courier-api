from marshmallow import fields
from sqlalchemy import Column, DateTime, Integer, String, func
from src.extensions import bcrypt, database, marshmallow


class ClientModel(database.Model):
    __tablename__ = 't_client'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(100))
    cellphone_no = Column(String(13))
    first_name = Column(String(40))
    middle_name = Column(String(30))
    last_name = Column(String(40))
    email = Column(String(30))
    province = Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    street = Column(String(50))
    landmarks = Column(String(50))
    updated_timestamp = Column(DateTime, nullable=True)
    registered_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, first_name, username, password, last_name, email, cellphone_no='', province='', city='',
                 district='', middle_name='', street='', landmarks='', **kwargs):
        super(ClientModel, self).__init__(**kwargs)
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.cellphone_no = cellphone_no
        self.province = province
        self.city = city
        self.district = district
        self.street = street
        self.landmarks = landmarks

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

    def __repr__(self):
        return '<Client %r>' % self.first_name


class ClientSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientModel
        strict = True

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)
    first_name = fields.Str(missing='')
    last_name = fields.Str(missing='')
    middle_name = fields.Str(missing='')
    email = fields.Str(missing='')
    cellphone_no = fields.Str(missing='')
    province = fields.Str(missing='')
    city = fields.Str(missing='')
    district = fields.Str(missing='')
    landmarks = fields.Str(missing='')
    updated_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
    registered_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
