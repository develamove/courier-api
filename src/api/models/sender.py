from src.extensions import database, marshmallow
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from marshmallow import fields


class SenderModel(database.Model):
    __tablename__ = 't_sender'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(60))
    cellphone_no = Column(String(13))
    email = Column(String(60))
    province = Column(String(100))
    city = Column(String(100))
    district = Column(String(100))
    street = Column(String(100))
    landmarks = Column(String(100))
    postal_code = Column(String(20))
    set_timestamp = Column(DateTime, nullable=True)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    delivery_id = database.Column(Integer, ForeignKey('t_delivery.id'))

    def __init__(self, full_name, cellphone_no, province, city, district, postal_code, delivery_id, email='', street='',
                 landmarks=''):
        self.full_name = full_name
        self.email = email
        self.cellphone_no = cellphone_no
        self.province = province
        self.city = city
        self.district = district
        self.street = street
        self.landmarks = landmarks
        self.delivery_id = delivery_id

    def __repr__(self):
        return '<Sender %r>' % self.full_name


class SenderSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = SenderModel
        strict = True

    id = fields.Int(dump_only=True)
    delivery_id = fields.Int(dump_only=True)
    email = fields.Str(missing='')
    cellphone_no = fields.Str(missing='')
    province = fields.Str(missing='')
    city = fields.Str(missing='')
    district = fields.Str(missing='')
    landmarks = fields.Str(missing='')
    set_timestamp = fields.DateTime()
    registered_timestamp = fields.DateTime(dump_only=True)
