from flask import Flask, request, render_template

app = Flask(__name__)

# Dummy data for storing recipes (you can replace this with a database)
recipes = []

@app.route('/')
def index():
    return render_template('index.html')
#--------------------------------------------------------------------------------
@app.route('/signin')
def signin():
    return render_template('signin.html')
#--------------------------------------------------------------------------------

@app.route('/signup')
def signup():
    
    return render_template('signup.html')
#--------------------------------------------------------------------------------
@app.route('/contact')
def contact():
   
    return render_template('contactus.html')
#--------------------------------------------------------------------------------
# View all recipes
@app.route('/recipes')
def view_recipes():
    return render_template('recipes.html', recipes=recipes)

#---------------------------------------------------------------------------------

# Add a recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    # Initialize error and success messages
    error_message = None
    success_message = None
    
    # Handle POST request
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        # Check if all fields are non-empty
        if name and ingredients and instructions:
            # Add recipe to the list
            recipes.append({'name': name, 'ingredients': ingredients, 'instructions': instructions})
            # Set success message
            success_message = 'Recipe added successfully!'
        else:
            # Set error message if any field is empty
            error_message = 'Error: Please provide name, ingredients, and instructions.'

    # Render template with error and success messages
    return render_template('add_recipe.html', error_message=error_message, success_message=success_message)

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
