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
    recipes_array = []
    recipes = Recipe.query.all()

    for recipe in recipes:
        recipes_array.append({'id': recipe.id, 'name': recipe.name})

    return render_template('recipes.html', recipes=recipes_array)

@bp.route('/get_items', methods=['POST'])
def get_items():
    req = request.get_json()
    recipe_id = req['id']

    if recipe_id:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe.id).join(Item).all()
        item_names = []
        for recipe_item in recipe_items:
            item_names.append(recipe_item.item.name)
    
    else:
        items = Item.query.all()
    
        item_names = []
        for item in items:
            item_names.append(item.name)
    
    return jsonify({'data': item_names})

'''
    #create dict with recipe name as key for all item names in that recipe
    for recipe_item_query in recipe_items_query:
        if recipe_item_query.recipe.id in recipe_items:
            recipe_items[recipe_item_query.recipe.id['items']].append(recipe_item_query.item.name)
        else:
            recipe_items.update({recipe_item_query.recipe.id :
                                    {'name': recipe_item_query.recipe.name,
                                    'items': [recipe_item_query.item.name]}})
'''


