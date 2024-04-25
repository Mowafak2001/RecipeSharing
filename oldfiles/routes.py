from app import app, db
from flask import render_template, redirect, url_for
from app.forms import AddRecipeForm, EditRecipeForm, DeleteRecipeForm, SearchRecipeForm
from app.models import Recipe

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(name=form.name.data, ingredients=form.ingredients.data, instructions=form.instructions.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_recipe.html', form=form)

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = EditRecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_recipe.html', form=form, recipe=recipe)

@app.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = DeleteRecipeForm()
    if form.validate_on_submit():
        db.session.delete(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('delete_recipe.html', form=form, recipe=recipe)

@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    form = SearchRecipeForm()
    if form.validate_on_submit():
        name = form.name.data
        recipes = Recipe.query.filter(Recipe.name.ilike(f'%{name}%')).all()
        return render_template('search_results.html', recipes=recipes)
    return render_template('search_recipe.html', form=form)
