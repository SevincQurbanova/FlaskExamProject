from app import create_app
from flask.cli import FlaskGroup
from app.models import db, User, Product, Category, Favorite, Review

app = create_app()
cli = FlaskGroup(app)

if __name__ == '__main__':
    from admin import *  # Import admin views
    app.run(debug=True)
