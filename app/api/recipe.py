from app.api import bp
from app.models import Item, Recipe, RecipeDateLog, RecipeItem, SelectedDatesLog
from flask import make_response, jsonify, request
from app import db
from sqlalchemy.exc import SQLAlchemyError



@bp.route('/api/recipes', methods=['GET', 'POST'])
def recipes_api():
    if request.method == 'GET':
        recipes = Recipe.query.all()
        
        recipes_data = []
        if recipes:
            for recipe in recipes:
                recipes_data.append({'id': recipe.id, 'name': recipe.name})
        else:
            recipes_data = None

        return make_response(jsonify({'data': recipes_data}), 200)

    elif request.method == 'POST':

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


