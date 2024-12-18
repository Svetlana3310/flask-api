from src import db, create_app  # Explicitly import from src

app = create_app()

# Create database tables
with app.app_context():
    db.create_all()
    print("Database initialized!")
