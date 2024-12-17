from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<User {self.name}>'


class ToDoItem(db.Model):
    __tablename__ = 'todo_items'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='todos')


# StoreModel
class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Relationship to ItemModel
    items = db.relationship(
        "ItemModel",
        back_populates="store",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Store {self.name}>"


# ItemModel
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Add ON DELETE CASCADE explicitly for clarity
    store_id = db.Column(
        db.Integer,
        db.ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationship back to StoreModel
    store = db.relationship(
        "StoreModel",
        back_populates="items"
    )

    def __repr__(self):
        return f"<Item {self.name}, Price: {self.price}, Store ID: {self.store_id}>"
