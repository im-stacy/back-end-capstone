import json
from flask import Blueprint, request, jsonify
from app import db
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.RecipeIngredient import RecipeIngredient

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
ingredients_bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@recipes_bp.route("", methods=["POST"])
def create_recipe():
    data = request.get_json()
    name = data.get("name")
    cooking_notes = data.get("cooking_notes")
    ingredients_data = data.get("ingredients")

    recipe = Recipe(name=name, cooking_notes=cooking_notes)
    db.session.add(recipe)
    db.session.commit()

    for ingredient_name, amount in ingredients_data.items():
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name)
            db.session.add(ingredient)
            db.session.commit()

        recipe_ingredient = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient.id, amount=amount)
        db.session.add(recipe_ingredient)
        db.session.commit()

    return jsonify({"message": "Recipe created successfully"}), 201



@recipes_bp.route("/recommend", methods=["POST"])
def recommend_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients")

    recipes = Recipe.query.join(RecipeIngredient).join(Ingredient).filter(
        Ingredient.name.in_(ingredients)
    ).group_by(Recipe.id).having(
        db.func.count(Ingredient.id) == len(ingredients)
    ).all()

    if not recipes:
        return jsonify({"message": "No recipes found with the specified ingredients"}), 404

    return jsonify([{"id": recipe.id, "name": recipe.name} for recipe in recipes]), 200


@recipes_bp.route("/", methods=["GET"])
def get_recipes_with_ingredients():
    recipes = Recipe.query.all()

    if not recipes:
        return jsonify({"message": "No recipes found in the database"}), 404

    recipes_data = []
    for recipe in recipes:
        ingredients = []
        for recipe_ingredient in recipe.ingredients:
            ingredient = Ingredient.query.get(recipe_ingredient.ingredient_id)
            ingredients.append({"name": ingredient.name, "amount": recipe_ingredient.amount})
        recipes_data.append({"id": recipe.id, "name": recipe.name, "ingredients": ingredients})

    return jsonify(recipes_data), 200


@recipes_bp.route("/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message": "Recipe deleted successfully"}), 200