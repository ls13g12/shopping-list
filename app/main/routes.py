from flask import render_template, make_response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Item, Recipe, RecipeItem
from app.main import bp
from app.main.forms import SelectDatesForm
from datetime import date, timedelta


@bp.route('/')
@bp.route('/list')
def list():
    recipe_items = RecipeItem.query.join(Item).all()
    items = []

    for recipe_item in recipe_items:
        item_data = {'name': recipe_item.item.name, 'quantity': recipe_item.quantity}

        if item_data in items:
            index = items.index(item_data)
            items[index]['quantity'] += recipe_item.quantity
        
        else:
            items.append(item_data)
            
    return render_template('list.html', items=items)

@bp.route('/recipes')
def recipes():
    #empty dictionary
    recipes_array = []
    recipes = Recipe.query.all()

    for recipe in recipes:
        recipes_array.append({'id': recipe.id, 'name': recipe.name})

    return render_template('recipes.html', recipes=recipes_array)


@bp.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html')


@bp.route('/get_recipes', methods=['POST'])
def get_recipes():

    recipes = Recipe.query.all()
    
    recipes_data = []
    if recipes:
        for recipe in recipes:
            recipes_data.append({'id': recipe.id, 'name': recipe.name})
    else:
        recipes_data = None

    return jsonify({'data': recipes_data})

@bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    #lower case recipe name from fetch request body
    req = request.get_json()
    recipe_name = req['recipe'].lower()

    try:
        recipe = Recipe.query.filter_by(name=recipe_name).first()

        #add recipe to db
        if not recipe:
            recipe = Recipe(name=recipe_name)
            db.session.add(recipe)
            db.session.commit()
            
            res = make_response(jsonify({}), 204)
            return res
        
        #return 409 conflict if recipe already exists
        if recipe:
            res = make_response(jsonify({"error": "Recipe already exists"}), 409)
            return res
    
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route('/remove_recipe', methods=['POST'])
def remove_recipe():
    req = request.get_json()
    recipe_id = req['recipe_id']

    #delete all items linked to recipe in RecipeItem table
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe:
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe.id).all()
        for recipe_item in recipe_items:
            db.session.delete(recipe_item)
        db.session.delete(recipe)
        db.session.commit()

    return jsonify(success=True), 200


@bp.route('/get_items', methods=['POST'])
def get_items():
    req = request.get_json()
    recipe_id = req['id']

    if recipe_id:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe.id).join(Item).all()
        items = []
        for recipe_item in recipe_items:
            items.append({'id': recipe_item.id, 'name': recipe_item.item.name})
    
    else:
        items = Item.query.all()
    
        items = []
        for item in items:
            items.append({'id': item.id, 'name': item.name})
    
    return jsonify({'data': items})

@bp.route('/add_item_to_recipe', methods=['POST'])
def add_item_to_recipe():
    req = request.get_json()
    recipe_id = req['recipe_id']
    item_name = req['item'].lower()

    #try query database
    try:
        item = Item.query.filter_by(name=item_name).first()
        if not item:
            item = Item(name=item_name)
            db.session.add(item)
            db.session.commit()

        recipe_item = RecipeItem.query.filter_by(item_id=item.id, recipe_id=recipe_id).first()
        if recipe_item:
            res = make_response(jsonify({"error": "Item already exists in recipe"}), 409)
            return res

        if not recipe_item:
            recipe_item = RecipeItem(item_id=item.id, recipe_id=recipe_id)
            db.session.add(recipe_item)
            db.session.commit()
            res = make_response(jsonify({}), 204)
            return res

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route('/remove_item_from_recipe', methods=['POST'])
def remove_item_from_recipe():
    req = request.get_json()
    recipe_item_id = req['recipe_item_id']


    recipe_item = RecipeItem.query.filter_by(id=recipe_item_id).first()
    if recipe_item:
        db.session.delete(recipe_item)
        db.session.commit()

    return jsonify(success=True), 200




