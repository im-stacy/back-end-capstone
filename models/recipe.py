from app import db
from flask import abort, make_response

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cooking_notes = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    ingredients = db.relationship('Ingredient', secondary='recipe_ingredient', lazy='subquery',
        backref=db.backref('recipes', lazy=True))
    

    