from flask import Blueprint, jsonify, request
from app import db
from app.models import ItemModel, StoreModel
from app.schemas.items_schema import ItemSchema

item_bp = Blueprint('item', __name__, url_prefix='/items')
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@item_bp.route('', methods=['GET'])
def get_all_items():
    """Get all items."""
    items = ItemModel.query.all()
    return items_schema.dump(items), 200


@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a single item by ID."""
    item = ItemModel.query.get_or_404(item_id)
    return item_schema.dump(item), 200


@item_bp.route('', methods=['POST'])
def create_item():
    """Create a new item."""
    data = request.get_json()
    item = item_schema.load(data, session=db.session)

    db.session.add(item)
    db.session.commit()
    return item_schema.dump(item), 201


@item_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item."""
    item = ItemModel.query.get_or_404(item_id)
    data = request.get_json()

    if 'name' in data:
        item.name = data['name']
    if 'price' in data:
        item.price = data['price']

    db.session.commit()
    return item_schema.dump(item), 200


@item_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item by ID."""
    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200
