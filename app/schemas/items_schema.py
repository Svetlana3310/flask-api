from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models import ItemModel


class ItemSchema(SQLAlchemySchema):
    class Meta:
        model = ItemModel
        load_instance = True  # Deserialize to SQLAlchemy objects

    id = auto_field()
    name = auto_field()
    price = auto_field()
    store_id = auto_field()
