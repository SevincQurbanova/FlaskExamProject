from flask_admin.contrib.sqla import ModelView
from app import flask_admin, db  # Import the renamed flask_admin and db
from app.models import Category, Product

# Add views to the admin interface
flask_admin.add_view(ModelView(Category, db.session))
flask_admin.add_view(ModelView(Product, db.session))
