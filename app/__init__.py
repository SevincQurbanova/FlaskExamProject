from flask import Flask
from flask import session  # Import session from flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin as FlaskAdmin  # Avoid naming conflict
from sqlalchemy import create_engine, text
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
flask_admin = FlaskAdmin()  # Rename admin instance to avoid conflict

def create_database_if_not_exists():
    # Create engine without specifying a database
    engine = create_engine('mysql+pymysql://root:12345@localhost')
    
    # Create database if it does not exist
    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS flaskdb"))
        print("Database 'flaskdb' checked or created.")

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/flaskdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Ensure the database is created before initializing the app
    create_database_if_not_exists()

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    flask_admin.init_app(app)  # Initialize Flask-Admin with the renamed instance

    # Enable CSRF protection
    csrf.init_app(app)

    # Context Processor
    @app.context_processor
    def inject_categories():
        from app.models import Category
        categories = Category.query.all()  # Fetch categories from the database
        return dict(categories=categories)

    # Context Processor for favorites count
    @app.context_processor
    def inject_favorites_count():
        user_id = session.get('user_id')
        if user_id:
            from app.models import Favorite  # Import Favorite here 
            favorites_count = Favorite.query.filter_by(user_id=user_id).count()
        else:
            favorites_count = 0
        return dict(favorites_count=favorites_count)

    # Import and register the Blueprint for routes
    from app.routes import routes_bp  # Ensure this import is after db and other extensions are initialized
    app.register_blueprint(routes_bp)
    return app


