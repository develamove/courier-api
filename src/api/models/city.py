from marshmallow import fields
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, func
from src.extensions import database, marshmallow


class CityModel(database.Model):
    __tablename__ = 't_city'

    id = Column(Integer, primary_key=True)
    province_id = Column(Integer, ForeignKey('t_province.id'), nullable=False)
    name = Column(String(50))
    is_pickup_available = Column(String(1))
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, province_id, name, is_pickup_available):
        self.province_id = province_id
        self.is_pickup_available = is_pickup_available
        self.name = name

    def __repr__(self):
        return '<City %r>' % self.name


class CitySchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = CityModel
        strict = True

    id = fields.Int(dump_only=True)
    name = fields.Str(missing='')
    is_pickup_available = fields.Str(missing='')
    created_timestamp = fields.DateTime(dump_only=True)
