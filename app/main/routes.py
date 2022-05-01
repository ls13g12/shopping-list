from flask import render_template, redirect,url_for, make_response, jsonify, request
from pendulum import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Item, Recipe, RecipeDateLog, RecipeItem, SelectedDatesLog
from app.main import bp
from datetime import datetime, timedelta


@bp.route('/')
@bp.route('/list')
def list():
    dates = SelectedDatesLog.query.order_by(SelectedDatesLog.timestamp.desc()).first()
    items = []
    dates = None
    if dates:
      items = get_items_for_dates(dates)
      dates = {'start_date': dates.start_date.strftime("%m/%d/%Y"), 'end_date': dates.end_date.strftime("%m/%d/%Y")}
     
    return render_template('list.html', items=items, dates=dates)

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


def get_items_for_dates(dates):
    recipe_dates = RecipeDateLog.query.filter(RecipeDateLog.date >= dates.start_date, RecipeDateLog.date <= dates.end_date).all()
    items = []

    for recipe_date in recipe_dates:
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe_date.recipe_id).join(Item).all()

        for recipe_item in recipe_items:
        
            item_data = {'name': recipe_item.item.name, 'quantity': recipe_item.quantity}

            if item_data in items:
                index = items.index(item_data)
                items[index]['quantity'] += recipe_item.quantity
            
            else:
                items.append(item_data)
    return items


@bp.route('/get_selected_dates', methods=['POST'])
def get_selected_dates():

    try:
        dates = SelectedDatesLog.query.order_by(SelectedDatesLog.timestamp.desc()).first()
        if dates:
            dates = {'start_date': dates.start_date.strftime("%m/%d/%Y"), 'end_date': dates.end_date.strftime("%m/%d/%Y")}
          
        res = make_response(jsonify({'dates': dates}), 200)
        return res
  
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res

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


@bp.route('/get_recipes_for_date', methods=['POST'])
def get_recipes_for_date():
    req = request.get_json()
    date_string = req['date_string']
    date = datetime.strptime(date_string, "%d/%m/%Y")
    tomorrow_date = date + timedelta(days=1)

    try:
        recipe_dates = RecipeDateLog.query.filter(RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date).join(Recipe).all()

        if recipe_dates:   
            res = make_response(jsonify({'data': [{'id': recipe_date.recipe_id, 'name': recipe_date.recipe.name} for recipe_date in recipe_dates]}), 200)
            return res

        else:
            res = make_response(jsonify({'data': None}), 204)
            return res
        
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route('/add_recipe_date', methods=['POST'])
def add_recipe_date():
    #lower case recipe name from fetch request body
    req = request.get_json()
    recipe_id = req['recipe_id']
    date_string = req['date_string']

    date = datetime.strptime(date_string, "%d/%m/%Y")
    tomorrow_date = date + timedelta(days=1)

    try:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_dates = RecipeDateLog.query.filter(RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date).all()

        if recipe_dates:   
            for recipe_date in recipe_dates:
                if recipe.id == recipe_date.recipe.id:
                    #duplicates currently not permitted - increase quantity in future
                    res = make_response(jsonify({"error": "Recipe already added"}), 409)
                    return res

        #add recipe_date to db
        recipe_date = RecipeDateLog(recipe_id=recipe.id, date = date)
        db.session.add(recipe_date)
        db.session.commit()
        
        res = make_response(jsonify({}), 204)
        return res


  
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route('/remove_recipe_date', methods=['POST'])
def remove_recipe_date():
    #lower case recipe name from fetch request body
    req = request.get_json()
    recipe_id = req['recipe_id']
    date_string = req['date_string']

    date = datetime.strptime(date_string, "%d/%m/%Y")
    tomorrow_date = date + timedelta(days=1)

    try:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_dates = RecipeDateLog.query.filter_by(recipe_id=recipe.id).filter(RecipeDateLog.date >= date, RecipeDateLog.date < tomorrow_date).all()

        if recipe_dates:   
            for recipe_date in recipe_dates:
                db.session.delete(recipe_date)
            db.session.commit()
            res = make_response(jsonify({}), 204)
            return res

        #duplicates currently not permitted - increase quantity in future
        res = make_response(jsonify({"error": "Recipe doesn't exist for date"}), 409)
        return res
  
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route('/select_new_dates', methods=['POST'])
def select_new_dates():
    #lower case recipe name from fetch request body
    req = request.get_json()
    start_date = req['start_date']
    end_date = req['end_date']
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")


    try:
        selected_dates = SelectedDatesLog(start_date=start_date, end_date=end_date)
        db.session.add(selected_dates)
        db.session.commit()

        #duplicates currently not permitted - increase quantity in future
        res = make_response(jsonify({}), 200)
        return res
  
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res

@bp.route('/select_new_dates_items', methods=['POST'])
def select_new_dates_items():
    #lower case recipe name from fetch request body
    req = request.get_json()
    start_date = req['start_date']
    end_date = req['end_date']
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    try:
        selected_dates = SelectedDatesLog(start_date=start_date, end_date=end_date)
        db.session.add(selected_dates)
        db.session.commit()

        #duplicates currently not permitted - increase quantity in future
        return redirect(url_for('main.list'))
  
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        res = make_response(jsonify({"error": error}), 500)
        return res


