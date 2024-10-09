from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.controllers import register_user, get_shop_data
from app.models import User, Product, ProductDetailImages, Favorite, Review, Contact, db
from app.forms import LoginForm, RegisterForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from sqlalchemy import or_

# Create a blueprint
routes_bp = Blueprint('routes_bp', __name__)



@routes_bp.route('/')
@routes_bp.route('/home', endpoint='home')
def shop():
    # Use the shop function to get data
    context = get_shop_data()
    return render_template('shop.html', **context)




@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instantiate the form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Debugging: Print email and password to check if they are correctly captured
        print(f"Login attempt with email: {email} and password: {password}")

        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Log the user in by storing info in session
            session['user_id'] = user.id
            session['username'] = user.name
            print(f"User {user.name} logged in successfully.")  # Debugging message
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes_bp.shop'))  # Redirect to the shop page after login
        else:
            print("Invalid login attempt.")  # Debugging message
            flash('Invalid email or password', 'danger')

    print("Form validation failed.")  # Debugging message
    return render_template('login.html', form=form)

@routes_bp.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes_bp.shop'))

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the email is already registered
        if User.query.filter_by(email=form.email.data).first():
            flash('Email address already registered.', 'danger')
            return redirect(url_for('routes_bp.register'))

        # Get data from form fields
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user instance
        new_user = User(name=name, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            print("User added to the database successfully")  # Debug message
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('routes_bp.login'))  # Redirect to the login page after registration
        except Exception as e:
            db.session.rollback()
            print(f"Error while adding user to the database: {e}")  # Print the actual error message
            flash('An error occurred while registering. Please try again.', 'danger')

    else:
        # If form validation fails, print errors
        print(form.errors)  # This will print validation errors to the console if there are any

    return render_template('register.html', form=form)


@routes_bp.route('/search')
def search():
    query = request.args.get('query')

    # If the search query is empty, redirect to the shop page
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('routes_bp.shop'))

    # Search products by name or description
    search_results = Product.query.filter(
        or_(
            Product.name.ilike(f'%{query}%'),
            Product.description.ilike(f'%{query}%')
        )
    ).all()

    if not search_results:
        flash('No products found matching your search.', 'warning')

    # Reuse the shop.html template to display the search results
    return render_template('shop.html', products=search_results, search_query=query)



@routes_bp.route('/add_to_favorite/<int:product_id>', methods=['POST'])
def add_to_favorite(product_id):
    user_id = session.get('user_id')  # Assuming the user is logged in and their ID is stored in the session

    if not user_id:
        flash('You need to log in to add products to your favorites.', 'danger')
        return redirect(url_for('routes_bp.login'))

    # Check if the product exists
    product = Product.query.get_or_404(product_id)

    # Check if the product is already in the user's favorites
    existing_favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_favorite:
        flash(f'{product.name} is already in your favorites.', 'warning')
    else:
        # Add product to the user's favorites
        favorite = Favorite(user_id=user_id, product_id=product.id)

        try:
            db.session.add(favorite)
            db.session.commit()
            flash(f'{product.name} has been added to your favorites.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the product to your favorites.', 'danger')
            print(f"Error: {e}")

    # Redirect back to the product detail page
    return redirect(url_for('routes_bp.detail', product_id=product.id))




@routes_bp.route('/product/<int:product_id>')
def detail(product_id):
    # Fetch the product from the database by ID
    product = Product.query.get_or_404(product_id)

    # Query all images associated with this product
    product_images = ProductDetailImages.query.filter_by(product_id=product_id).all()

    # Fetch reviews for this product
    reviews = Review.query.filter_by(product_id=product_id, active='1').all()
    review_count = len(reviews)

    # Fetch related products from the same category, excluding the current product
    related_products = Product.query.filter(
        Product.category_id == product.category_id,  # Same category
        Product.id != product_id  # Exclude the current product
    ).limit(8).all()

    # Pass the product to the template
    return render_template('detail.html', 
                           product=product, 
                           product_images=product_images, 
                           reviews=reviews, 
                           review_count=review_count, 
                           related_products=related_products)



@routes_bp.route('/favorite')
def favorite():
    user_id = session.get('user_id')  # Assuming you store user_id in session
    if not user_id:
        # Redirect to login if user is not authenticated
        return redirect(url_for('routes_bp.login'))

    # Get favorite products for the user
    favorite_products = Favorite.query.filter_by(user_id=user_id).all()

    # You can also join the Product table to get more details about the product
    favorite_products_with_details = [
        { 
            'id': fav.product.id,  # Include the product ID here
            'name': fav.product.name,
            'price': fav.product.price,
            'image': fav.product.img_path
        }
        for fav in favorite_products
    ]

    return render_template('favorites.html', favorite_products=favorite_products_with_details)

@routes_bp.route('/remove_favorite/<int:product_id>', methods=['POST'])
def remove_favorite(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('routes_bp.login'))

    # Find the favorite entry and remove it
    favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()

    return redirect(url_for('routes_bp.favorite'))

@routes_bp.route('/add_review/<int:product_id>', methods=['POST'])
def add_review(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'You need to log in.'}), 401  # Returning JSON for AJAX error

    review_text = request.form.get('review')
    if not review_text:
        return jsonify({'error': 'Review cannot be empty.'}), 400  # Returning JSON for AJAX error

    new_review = Review(user_id=user_id, product_id=product_id, review=review_text)
    try:
        db.session.add(new_review)
        db.session.commit()

        # Fetch updated reviews to send back in the AJAX response
        reviews = Review.query.filter_by(product_id=product_id).all()
        review_count = len(reviews)

        # Render the reviews_section partial and send it back to the client
        reviews_html = render_template('partials/reviews_section.html', reviews=reviews, review_count=review_count)
        
        return jsonify({'reviews_html': reviews_html, 'review_count': review_count}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while submitting your review.'}), 500


@routes_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Process the form data
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('routes_bp.contact'))  # Redirect after form submission
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your message. Please try again later.', 'danger')

    return render_template('contact.html', form=form)

