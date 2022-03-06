from flask import render_template, redirect, url_for, jsonify, request
from app import db
from app.models import Item, Recipe, RecipeItem
from app.main import bp


@bp.route('/')
@bp.route('/list')
def list():
    recipe_items = RecipeItem.query.join(Item).all()
    return render_template('list.html', recipe_items=recipe_items)

@bp.route('/recipes')
def recipes():
    #empty dictionary
    recipe_items = {}
    recipe_items_query = RecipeItem.query.join(Item).join(Recipe).all()

    #create dict with recipe name as key for all item names in that recipe
    for recipe_item_query in recipe_items_query:
        if recipe_item_query.recipe.id in recipe_items:
            recipe_items[recipe_item_query.recipe.id['items']].append(recipe_item_query.item.name)
        else:
            recipe_items.update({recipe_item_query.recipe.id :
                                    {'name': recipe_item_query.recipe.name,
                                    'items': [recipe_item_query.item.name]}})

    return render_template('recipes.html', recipe_items=recipe_items)

