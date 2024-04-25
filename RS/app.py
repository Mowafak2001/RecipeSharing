from flask import Flask, render_template, request, redirect, session, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456789@localhost:3306/recipe'  
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
    email = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()





#--------------------------------------------------------------------------
# Dummy data for storing recipes (you can replace this with a database)
recipes = []

@app.route('/')
def index():
    return render_template('index.html')
#--------------------------------------------------------------------------------
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    return decorated_function
#--------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    # Remove the 'logged_in' key from the session
    session.pop('logged_in', None)
    # Redirect to the home page or any other desired page after logout
    return redirect(url_for('index'))
#--------------------------------------------------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error = "This email is already registered. Please use a different email."
            return render_template('signup.html', error=error)
        
        # Create a new user object
        new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to the signin page after successful registration
        return redirect(url_for('signin'))
    
    # For GET requests, render the signup page
    else:
        return render_template('signup.html')

#--------------------------------------------------------------------------------

@app.route('/contact')
@login_required
def contact():
   
    return render_template('contactus.html')

#--------------------------------------------------------------------------------
@app.route('/aboutus')
def aboutus():
   
    return render_template('aboutus.html')
#--------------------------------------------------------------------------------
# View all recipes
@app.route('/recipes')
@login_required

def view_recipes():
    return render_template('recipes.html', recipes=recipes)

#---------------------------------------------------------------------------------

# Add a recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    error_message = None  # Initialize error message
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        if name and ingredients and instructions:  # Ensure all fields are non-empty
            recipes.append({'name': name, 'ingredients': ingredients, 'instructions': instructions})
            return render_template('add_success_message.html')  # Render the add_success_message template
        else:
            error_message = 'Error: Please provide name, ingredients, and instructions.'

    return render_template('add_recipe.html', error_message=error_message)

#----------------------------------------------------------------------------------------------------------------------------

# Edit a recipe
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # Check if the recipe_id is within the valid range
    if recipe_id < 0 or recipe_id >= len(recipes):
        return 'Error: Recipe ID is invalid.'

    if request.method == 'POST':
        if 'name' in request.form and 'ingredients' in request.form and 'instructions' in request.form:
            name = request.form['name']
            ingredients = request.form['ingredients']
            instructions = request.form['instructions']
            recipes[recipe_id] = {'name': name, 'ingredients': ingredients, 'instructions': instructions}
            return render_template('edit_success_message.html')  # Render the edit_success_message template

    return render_template('edit_recipe.html', recipe=recipes[recipe_id], recipe_id=recipe_id)

#------------------------------------------------------------------------------------------------------------------

# View a recipe details
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    if recipe_id < 0 or recipe_id >= len(recipes):
        return 'Error: Recipe ID is invalid.'
    return render_template('recipe_details.html', recipe=recipes[recipe_id])

#------------------------------------------------------------------------------------------------------------------

# Remove a recipe
@app.route('/remove_recipe/<int:recipe_id>')
def remove_recipe(recipe_id):
    if recipe_id < 0 or recipe_id >= len(recipes):
        return 'Error: Recipe ID is invalid.'

#---------------------------------------------------------------------------------------------------------------------

    del recipes[recipe_id]
    # Render the remove_success_message template
    return render_template('remove_success_message.html')

#---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
