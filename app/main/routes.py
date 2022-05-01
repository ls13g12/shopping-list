from flask import render_template, redirect, url_for, make_response, jsonify, request
from pendulum import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Item, Recipe, RecipeDateLog, RecipeItem, SelectedDatesLog
from app.main import bp
from datetime import datetime, timedelta


@bp.route("/")
@bp.route("/list")
def list():
    dates = SelectedDatesLog.query.order_by(SelectedDatesLog.timestamp.desc()).first()
    items = []
    if dates:
        items = get_items_for_dates(dates)
        dates = {
            "start_date": dates.start_date.strftime("%m/%d/%Y"),
            "end_date": dates.end_date.strftime("%m/%d/%Y"),
        }

    return render_template("list.html", items=items, dates=dates)


@bp.route("/recipes")
def recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)


@bp.route("/calendar")
def calendar():
    return render_template("calendar.html")


def get_items_for_dates(dates):
    recipe_dates = RecipeDateLog.query.filter(
        RecipeDateLog.date >= dates.start_date, RecipeDateLog.date <= dates.end_date
    ).all()
    items = []

    for recipe_date in recipe_dates:
        recipe_items = (
            RecipeItem.query.filter_by(recipe_id=recipe_date.recipe_id).join(Item).all()
        )

        for recipe_item in recipe_items:

            item_data = {
                "name": recipe_item.item.name,
                "quantity": recipe_item.quantity,
            }

            if item_data in items:
                index = items.index(item_data)
                items[index]["quantity"] += recipe_item.quantity

            else:
                items.append(item_data)
    return items
