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
    if request.method == 'POST':
        if 'name' in request.form and 'ingredients' in request.form and 'instructions' in request.form:
            name = request.form['name']
            ingredients = request.form['ingredients']
            instructions = request.form['instructions']
            recipes.append({'name': name, 'ingredients': ingredients, 'instructions': instructions})
            # Construct success message with links
            success_message = 'Recipe added successfully! <a href="/">Home</a> | <a href="/recipes">View All Recipes</a>'
            return success_message
        else:
            return 'Error: Please provide name, ingredients, and instructions.'
    return render_template('add_recipe.html')

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
            return 'Recipe edited successfully! <a href="/">Home</a> | <a href="/recipes">View All Recipes</a>'

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
    # Render the success message template
    return render_template('success_message.html')

#---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
