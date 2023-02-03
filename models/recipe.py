from app import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cooking_notes = db.Column(db.Text)
    ingredients = db.relationship("RecipeIngredient", backref="recipe", lazy=True)