from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddRecipeForm(FlaskForm):
    name = StringField('Recipe Name:', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients:', validators=[DataRequired()])
    instructions = TextAreaField('Instructions:', validators=[DataRequired()])
    submit = SubmitField('Add Recipe')

class EditRecipeForm(FlaskForm):
    name = StringField('Recipe Name:', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients:', validators=[DataRequired()])
    instructions = TextAreaField('Instructions:', validators=[DataRequired()])
    submit = SubmitField('Update Recipe')

class DeleteRecipeForm(FlaskForm):
    name = StringField('Recipe Name:', validators=[DataRequired()])
    submit = SubmitField('Delete Recipe')

class SearchRecipeForm(FlaskForm):
    name = StringField('Recipe Name:', validators=[DataRequired()])
    submit = SubmitField('Search Recipe')
