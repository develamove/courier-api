from marshmallow import fields
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, func
from src.extensions import database, marshmallow


class DistrictModel(database.Model):
    __tablename__ = 't_district'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('t_city.id'), nullable=False)
    name = Column(String(50))
    postal_code = Column(String(50))
    is_pickup_available = Column(String(1))
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, city_id, name, postal_code, is_pickup_available, **kwargs):
        super(DistrictModel, self).__init__(**kwargs)
        self.city_id = city_id
        self.name = name
        self.postal_code = postal_code
        self.is_pickup_available = is_pickup_available

    def __repr__(self):
        return '<District %r>' % self.name


class DistrictSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = DistrictModel
        strict = True

    id = fields.Int(dump_only=True)
    name = fields.Str(missing='')
    postal_code = fields.Str(missing='')
    is_pickup_available = fields.Str(missing='')
    created_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
