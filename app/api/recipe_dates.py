from app.api import bp
from app.models import Recipe, RecipeDateLog
from flask import make_response, jsonify, request
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


@bp.route("/get_recipes_for_date", methods=["POST"])
def get_recipes_for_date():
    req = request.get_json()
    date_string = req["date_string"]
    date = datetime.strptime(date_string, "%d/%m/%Y")
    tomorrow_date = date + timedelta(days=1)

    try:
        recipe_dates = (
            RecipeDateLog.query.filter(
                RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date
            )
            .join(Recipe)
            .all()
        )

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

        else:
            res = make_response(jsonify({"data": None}), 204)
            return res

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route("/add_recipe_date", methods=["POST"])
def add_recipe_date():
    # lower case recipe name from fetch request body
    req = request.get_json()
    recipe_id = req["recipe_id"]
    date_string = req["date_string"]

    date = datetime.strptime(date_string, "%d/%m/%Y")
    tomorrow_date = date + timedelta(days=1)

    try:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_dates = RecipeDateLog.query.filter(
            RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date
        ).all()

        if recipe_dates:
            for recipe_date in recipe_dates:
                if recipe.id == recipe_date.recipe.id:
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


@bp.route("/remove_recipe_date", methods=["POST"])
def remove_recipe_date():
    # lower case recipe name from fetch request body
    req = request.get_json()
    recipe_id = req["recipe_id"]
    date_string = req["date_string"]

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
