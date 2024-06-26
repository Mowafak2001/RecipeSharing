# Imports
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

# App configuration
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipesharing.sqlite3'

# Database setup
db = SQLAlchemy(app)

# Define models for User, ContactUs, and Recipe tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    reason = db.Column(db.String(200), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)  # Add email field back to Recipe model
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Decorator for login required routes
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    return decorated_function

# Route: Homepage
@app.route('/')
def index():
    return render_template('homepage.html')

# Route: Sign In
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Authentication logic
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['logged_in'] = True
            session['email'] = email  # Set the email session variable
            return jsonify({'status': 'success', 'message': 'Login successful'})
        
        # If email or password is incorrect
        error = 'Invalid email or password. Please try again.'
        return render_template('signin.html', error=error)
    
    # For GET requests
    return render_template('signin.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)  # Remove the email session variable on logout
    return redirect(url_for('index'))

# Route: Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error = "This email is already registered. Please use a different email."
            return render_template('signup.html', error=error)
        
        new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('signin'))
    
    return render_template('signup.html')

# Route: Contact Us (Accessible after login)
@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        reason = request.form['reason']

        new_contact = ContactUs(first_name=first_name, last_name=last_name, email=email, reason=reason)
        db.session.add(new_contact)
        db.session.commit()
        #flash('Your contact information has been submitted.','success')
        #flash('Your contact information has been submitted.', 'success')
        print(new_contact)
        return redirect(url_for('contact'))
    
    return render_template('contactus.html')

# Route: About Us
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# Route: Homepage
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

# Route: View all recipes (Accessible after login)
@app.route('/recipes')
@login_required
def view_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

# Route: View recipe details
@app.route('/recipe/<int:recipe_id>')
def view_recipe_detail(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return render_template('error.html', message="Recipe not found.")
    return render_template('recipe_details.html', recipe=recipe)

# Route: Add a new recipe (Accessible after login)
@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    error_message = None
    success_message = None
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        email = session.get('email')  # Get the email from the session

        if name and ingredients and instructions:
            new_recipe = Recipe(name=name, email=email, ingredients=ingredients, instructions=instructions)
            db.session.add(new_recipe)
            db.session.commit()
            success_message = 'Recipe added successfully!'     
        else:
            error_message = 'Error: One or more fields are empty.'

    return render_template('add_recipe.html', error_message=error_message, success_message=success_message)

# Route: Edit a recipe (Accessible after login)
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET'])
@login_required
def edit_recipe_form(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('edit_recipe.html', recipe=recipe, recipe_id=recipe_id)

# Route: Update a recipe (Accessible after login)
@app.route('/edit_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def edit_recipe(recipe_id):
    # Fetch the recipe from the database using recipe_id
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Update the recipe with the form data
    recipe.name = request.form.get('name')
    recipe.ingredients = request.form.get('ingredients')
    recipe.instructions = request.form.get('instructions')

    # Commit the changes to the database
    db.session.commit()

    # Redirect to a page displaying the edited recipe or to the list of all recipes
    return redirect(url_for('view_recipes'))

# Route: Search for recipes
@app.route('/search')
def search():
    query = request.args.get('query')
    filtered_recipes = Recipe.query.filter(
        (Recipe.name.ilike(f'%{query}%')) | (Recipe.ingredients.ilike(f'%{query}%'))).all()
    return render_template('search_results.html', query=query, recipes=filtered_recipes)

# Route: Remove a recipe (Accessible after login)
@app.route('/remove_recipe/<int:recipe_id>')
def remove_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return 'Error: Recipe ID is invalid.'

    db.session.delete(recipe)
    db.session.commit()
    return render_template('remove_success_message.html')

# Main function
if __name__ == '__main__':
    app.run(debug=True)








