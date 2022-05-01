from app.api import bp
from app.models import Item, Recipe, RecipeDateLog, RecipeItem, SelectedDatesLog
from flask import make_response, jsonify, request
from app import db
from sqlalchemy.exc import SQLAlchemyError


@bp.route("/api/recipes", methods=["GET"])
def get_recipes():
    if request.method == "GET":
        recipes = Recipe.query.all()

        recipes_data = []
        if recipes:
            for recipe in recipes:
                recipes_data.append({"id": recipe.id, "name": recipe.name})
        else:
            recipes_data = None

        return make_response(jsonify({"data": recipes_data}), 200)


@bp.route("/api/recipes", methods=["POST"])
def add_recipe():

    if request.method == "POST":
        # lower case recipe name from fetch request body
        body = request.get_json()
        recipe_name = body["recipe"].lower()

        try:
            recipe = Recipe.query.filter_by(name=recipe_name).first()

            # add recipe to db
            if not recipe:
                recipe = Recipe(name=recipe_name)
                db.session.add(recipe)
                db.session.commit()

                res = make_response(jsonify({}), 204)
                return res

            # return 409 conflict if recipe already exists
            if recipe:
                res = make_response(jsonify({"error": "Recipe already exists"}), 409)
                return res

        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            res = make_response(jsonify({"error": error}), 500)
            return res

    return make_response(jsonify({}), 500)


@bp.route("/api/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe_id = id

    # delete all items linked to recipe in RecipeItem table
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe:
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe.id).all()
        for recipe_item in recipe_items:
            db.session.delete(recipe_item)
        db.session.delete(recipe)
        db.session.commit()

    return make_response(jsonify({}), 204)
