from marshmallow import fields
from sqlalchemy import func, Column, DateTime, ForeignKey, Integer, String
from src.extensions import database, marshmallow


class SenderModel(database.Model):
    __tablename__ = 't_sender'

    id = Column(Integer, primary_key=True)
    delivery_id = database.Column(Integer, ForeignKey('t_delivery.id'))
    full_name = Column(String(60))
    cellphone_no = Column(String(13))
    email = Column(String(60))
    province = Column(String(100))
    city = Column(String(100))
    district = Column(String(100))
    street = Column(String(100))
    landmarks = Column(String(100))
    postal_code = Column(String(20))
    updated_timestamp = Column(DateTime, nullable=True)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, delivery_id, full_name, cellphone_no, province, city, district, street, postal_code, email='',
                 landmarks='', **kwargs):
        super(SenderModel, self).__init__(**kwargs)
        self.delivery_id = delivery_id
        self.full_name = full_name
        self.email = email
        self.cellphone_no = cellphone_no
        self.province = province
        self.city = city
        self.district = district
        self.street = street
        self.landmarks = landmarks
        self.postal_code = postal_code

    def __repr__(self):
        return '<Sender %r>' % self.full_name


class SenderSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = SenderModel
        strict = True

    id = fields.Int(dump_only=True)
    delivery_id = fields.Int(dump_only=True)
    full_name = fields.Str(missing='')
    cellphone_no = fields.Str(missing='')
    email = fields.Str(missing='')
    province = fields.Str(missing='')
    city = fields.Str(missing='')
    district = fields.Str(missing='')
    street = fields.Str(missing='')
    landmarks = fields.Str(missing='')
    postal_code = fields.Str(missing='')
    updated_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
    created_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
