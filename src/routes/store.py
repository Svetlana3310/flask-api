from flask import Blueprint, jsonify, request
from src import db
from src.models import StoreModel
from src.schemas.store_schema import StoreSchema
from flask_jwt_extended import jwt_required

store_bp = Blueprint('store', __name__, url_prefix='/stores')
store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)


@store_bp.route('', methods=['GET'])
def get_all_stores():
    """Get all stores."""
    stores = StoreModel.query.all()
    return stores_schema.dump(stores), 200


@store_bp.route('/<int:store_id>', methods=['GET'])
def get_store(store_id):
    """Get a single store by ID."""
    store = StoreModel.query.get_or_404(store_id)
    return store_schema.dump(store), 200


@store_bp.route('', methods=['POST'])
@jwt_required()
def create_store():
    """Create a new store."""
    data = request.get_json()
    store = store_schema.load(data, session=db.session)

    db.session.add(store)
    db.session.commit()
    return store_schema.dump(store), 201


@store_bp.route('/<int:store_id>', methods=['PUT'])
@jwt_required()
def update_store(store_id):
    """Update an existing store."""
    store = StoreModel.query.get_or_404(store_id)
    data = request.get_json()

    if 'name' in data:
        store.name = data['name']

    db.session.commit()
    return store_schema.dump(store), 200


@store_bp.route('/<int:store_id>', methods=['DELETE'])
@jwt_required()
def delete_store(store_id):
    """Delete a store by ID."""
    try:
        store = StoreModel.query.get_or_404(store_id)
        print(f"Items associated with store {store_id}: {
              [item.name for item in store.items]}")
        db.session.delete(store)
        db.session.commit()
        return jsonify({"message": "Store deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
