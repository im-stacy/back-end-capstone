from app import db
from flask import abort, make_response 


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recipes = db.relationship('Recipe', secondary='recipe_ingredient', lazy='subquery',
        backref=db.backref('ingredients', lazy=True))
