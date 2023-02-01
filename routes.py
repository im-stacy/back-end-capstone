from os import abort
import os
from flask import Blueprint, request, jsonify, make_response
from app import db
from models.recipe import Recipe
from models.ingredient import Ingredient
import requests


recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
ingredients_bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")

# helper function
def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400)) 

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404)) 

    return model

# for recipe 
@recipes_bp.route("", methods = ["POST"])
def create_recipe():
    name = request.json.get('name', '')
    cooking_notes = request.json.get('cooking_notes', '')
    ingredients = request.json.get('ingredients', {})

    # validate inputs
    if not name or not ingredients:
        return make_response(jsonify({'error': 'Invalid input'}), 400)

    recipe = Recipe(name = name, cooking_notes = cooking_notes)
    
    # add ingredients to the recipe
    for ingredient_name, ingredient_amount in ingredients.items():
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name, amount=ingredient_amount)
            db.session.add(ingredient)
        recipe.ingredients.append(ingredient)

    db.session.add(recipe)
    db.session.commit()

    return make_response(jsonify({'new recipe':{
                                            'id': recipe.id,
                                            'name': recipe.name,
                                            'ingredients': recipe.ingredients}}), 201)

    