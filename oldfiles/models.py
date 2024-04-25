from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User (UserMixin, db.Model):
   __tablename__ = 'user'
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(120), unique=True, nullable=False)
   FirstName = db.Column(db.String(50), unique=False, nullable=False)
   LastName = db.Column(db.String(50), unique=False, nullable=False)
   passwordHash = db.Column(db.String(120), unique=False, nullable=False)
   role = db.Column(db.String(50), unique=False, nullable=False)


class Recipe(db.Model):
   __tablename__ ='recipe'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   title = db.Column(db.String(50), unique=False, nullable=False)
   description = db.Column(db.String(50), unique=False, nullable=False)
   instrucions = db.Column(db.String(50), unique=False, nullable=False)






class ingredient (db.Model):
   __tablename__ = 'ingredient'
   id = db.Column(db.Integer, primary_key=True)
   ingredient_name = db.Column(db.String(50), unique=False, nullable=False)
   ingredient_category = db.Column(db.String(50), unique=False, nullable=False)
   description = db.Column(db.String(50), unique=False, nullable=False)




class Complaint(db.Model):
   __tablename__ = 'complaint'
   id = db.Column(db.Integer, primary_key=True)
   complainant_email = db.Column(db.String(120), db.ForeignKey('user.email'), unique=False, nullable=False)
   respondent_email = db.Column(db.String(120), db.ForeignKey('user.email'), unique=False, nullable=False)
   date = db.Complaint(db.String(120), nullable=False)
   description = db.Column(db.String(120), nullable=False)




  
class Like_Dislike(db.Model):
   __tablename__ = 'like_dislike'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
   recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), unique=False, nullable=False)
   reaction = db.Column(db.String(50), unique=False, nullable=False)
