from app.api import bp
from app.models import Recipe, RecipeItem, RecipeDateLog
from flask import make_response, jsonify, request
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


#get all recipes or recipes for a specified date
@bp.route("/api/recipes", methods=["GET"])
def get_recipes():

    date_string = request.args.get("date")
    if date_string:
        date = datetime.strptime(date_string, "%d/%m/%Y")
        tomorrow_date = date + timedelta(days=1)

        #query db for recipes chosen for date
        try:
            recipe_dates = (
                RecipeDateLog.query.filter(
                    RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date
                )
                .join(Recipe)
                .all()
            )
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            res = make_response(jsonify({"error": error}), 500)
            return res

        if recipe_dates:
            res = make_response(
                jsonify(
                    {
                        "data": [
                            {
                                "id": recipe_date.recipe_id,
                                "name": recipe_date.recipe.name,
                            }
                            for recipe_date in recipe_dates
                        ]
                    }
                ),
                200,
            )
            return res

        # it is valid for a date to not have any recipes yet
        else:
            res = make_response(jsonify({"data": None}), 204)
            return res

    # returns all recipes if no date argument given
    recipes = Recipe.query.all()

    return make_response(
        jsonify(
            {"data": [{"id": recipe.id, "name": recipe.name} for recipe in recipes]}
        ),
        200,
    )

#add recipe to db or link recipe to a specified date via junction table
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

#delete recipe if no args
#delete recipe from date args if args
@bp.route("/api/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe_id = id
    args = request.args

    if args:
        date_string = args.get("date")
        date = datetime.strptime(date_string, "%d/%m/%Y")
        tomorrow_date = date + timedelta(days=1)

        try:
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            recipe_dates = (
                RecipeDateLog.query.filter_by(recipe_id=recipe.id)
                .filter(RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date)
                .all()
            )

            if recipe_dates:
                for recipe_date in recipe_dates:
                    db.session.delete(recipe_date)
                db.session.commit()
                res = make_response(jsonify({}), 204)
                return res

            # duplicates currently not permitted - increase quantity in future
            res = make_response(jsonify({"error": "Recipe doesn't exist for date"}), 409)
            return res

        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            res = make_response(jsonify({"error": error}), 500)
            return res

    # delete all items linked to recipe in RecipeItem table
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe:
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe.id).all()
        for recipe_item in recipe_items:
            db.session.delete(recipe_item)
        db.session.delete(recipe)
        db.session.commit()

    return make_response(jsonify({}), 204)

#add recipe 
@bp.route("/api/recipes/<int:id>", methods=["POST"])
def add_recipe_to_date(id):
    recipe_id = id
    date_string = request.args.get("date")
    print(date_string)

    date = datetime.strptime(date_string, "%d/%m/%Y")
    tomorrow_date = date + timedelta(days=1)

    try:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        print(recipe)
        recipe_dates = RecipeDateLog.query.filter(
            RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date
        ).all()

        if recipe_dates:
            for recipe_date in recipe_dates:
                if recipe.id == recipe_date.recipe_id:
                    # duplicates currently not permitted - increase quantity in future
                    res = make_response(jsonify({"error": "Recipe already added"}), 409)
                    return res

        # add recipe_date to db
        recipe_date = RecipeDateLog(recipe_id=recipe.id, date=date)
        db.session.add(recipe_date)
        db.session.commit()

        res = make_response(jsonify({}), 204)
        return res

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        res = make_response(jsonify({"error": error}), 500)
        return res
