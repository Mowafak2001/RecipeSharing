from flask import Flask, render_template, request, redirect, session, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipesharing.sqlite3'

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
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Your authentication logic here...
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['logged_in'] = True
            return jsonify({'status': 'success', 'message': 'Login successful'})
        
        # If email or password is incorrect, render the signin page with an error message
        error = 'Invalid email or password. Please try again.'
        return render_template('signin.html', error=error)
    
    # For GET requests, simply render the signin.html template
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

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

@app.route('/contact')
@login_required
def contact():
    return render_template('contactus.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/recipes')
@login_required
def view_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    error_message = None
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        if name and ingredients and instructions:
            new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
            db.session.add(new_recipe)
            db.session.commit()
            return render_template('add_success_message.html')
        else:
            error_message = 'Error: Please provide name, ingredients, and instructions.'

    return render_template('add_recipe.html', error_message=error_message)

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return 'Error: Recipe ID is invalid.'

    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        if name and ingredients and instructions:
            recipe.name = name
            recipe.ingredients = ingredients
            recipe.instructions = instructions
            db.session.commit()
            return render_template('edit_success_message.html')

    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return 'Error: Recipe ID is invalid.'
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/search')
def search():
    query = request.args.get('query')
    filtered_recipes = Recipe.query.filter(
        (Recipe.name.ilike(f'%{query}%')) | (Recipe.ingredients.ilike(f'%{query}%'))).all()
    return render_template('search_results.html', query=query, recipes=filtered_recipes)

@app.route('/remove_recipe/<int:recipe_id>')
def remove_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return 'Error: Recipe ID is invalid.'

    db.session.delete(recipe)
    db.session.commit()
    return render_template('remove_success_message.html')

if __name__ == '__main__':
    app.run(debug=True)

