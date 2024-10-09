from flask import redirect, url_for, request
from app.models import db, User, Product, Category, Favorite, Review  # Updated import path
from sqlalchemy import func  # Import function for counting
import os

def create_tables_if_not_exist():
    if not os.path.exists('migrations'):
        # Run DB migrations if they don't exist
        os.system('flask db init')
        os.system('flask db migrate')
        os.system('flask db upgrade')

def register_user(surname, name, patronymic, username, email, password):
    user = User(surname=surname, name=name, patronymic=patronymic, username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))

def get_shop_data():
    # Fetch all categories from the database
    categories = Category.query.all()

    # Fetch categories and the count of products in each category
    categories_with_counts = db.session.query(
        Category.id,
        Category.name,
        func.count(Product.id).label('product_count')
    ).outerjoin(Product, Product.category_id == Category.id) \
     .group_by(Category.id).all()

    
    # Get the category ID from the request, if present
    category_id = request.args.get('category')
    
    # if category_id:
    #     try:
    #         # Convert the category_id to an integer for the database query
    #         category_id = int(category_id)
    #     except ValueError:
    #         # If conversion fails, return an empty list of products or handle the error
    #         products = []
    #     else:
    #         # Ensure the category exists before querying products
    #         if Category.query.get(category_id):
    #             # Filter products by the selected category
    #             products = Product.query.filter_by(category_id=category_id).all()
    #         else:
    #             # If the category doesn't exist, return an empty product list
    #             products = []
    # else:
    #     # If no category filter, get all products
    #     products = Product.query.all()

    if category_id:
        try:
            # Convert the category_id to an integer for the database query
            category_id = int(category_id)
        except ValueError:
            # If conversion fails, return an empty list of products or handle the error
            products = []
        else:
            # Ensure the category exists before querying products
            if Category.query.get(category_id):
                # Filter products by the selected category
                products = Product.query.filter_by(category_id=category_id).all()
            else:
                # If the category doesn't exist, return an empty product list
                products = []
    else:
        # If no category filter, get all products
        products = Product.query.all()


    # Return context data to be passed to the template
    context = {
        'categories': categories,
        'categories_with_count': categories_with_counts,  # Pass categories with product counts
        'products': products
    }

   
    return context
