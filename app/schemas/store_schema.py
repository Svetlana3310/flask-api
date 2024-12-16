from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models import StoreModel


class StoreSchema(SQLAlchemySchema):
    class Meta:
        model = StoreModel
        load_instance = True  # Deserialize to SQLAlchemy objects

    id = auto_field()
    name = auto_field()
