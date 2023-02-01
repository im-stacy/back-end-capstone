from app import db


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
