from app.api import bp
from app.models import Item, Recipe, RecipeItem
from flask import make_response, jsonify, request
from app import db
from sqlalchemy.exc import SQLAlchemyError


@bp.route("/api/recipes/<int:id>/items", methods=["GET"])
def get_items(id):
    recipe_id = id

    if recipe_id:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe_items = RecipeItem.query.filter_by(recipe_id=recipe.id).join(Item).all()
        items = []
        for recipe_item in recipe_items:
            items.append({
              "recipe_id": recipe_id,
              "item_id": recipe_item.item.id, 
              "name": recipe_item.item.name})

    else:
        items = Item.query.all()

        items = []
        for item in items:
            items.append({"id": item.id, "name": item.name})

    return jsonify({"data": items})

@bp.route("/api/recipes/<int:id>/items", methods=["POST"])
def add_item_to_recipe(id):
    body = request.get_json()
    recipe_id = id
    item_name = body["item"].lower()

    # try query database
    try:
        item = Item.query.filter_by(name=item_name).first()
        if not item:
            item = Item(name=item_name)
            db.session.add(item)
            db.session.commit()

        recipe_item = RecipeItem.query.filter_by(
            item_id=item.id, recipe_id=recipe_id
        ).first()
        if recipe_item:
            res = make_response(
                jsonify({"error": "Item already exists in recipe"}), 409
            )
            return res

        if not recipe_item:
            recipe_item = RecipeItem(item_id=item.id, recipe_id=recipe_id)
            db.session.add(recipe_item)
            db.session.commit()
            res = make_response(jsonify({}), 204)
            return res

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        res = make_response(jsonify({"error": error}), 500)
        return res
    
    return make_response(jsonify({}), 500)


@bp.route("/api/recipes/<int:recipe_id>/items/<int:item_id>", methods=["DELETE"])
def remove_item_from_recipe(recipe_id, item_id):

    recipe_item = RecipeItem.query.filter_by(recipe_id=recipe_id, item_id=item_id).first()
    if recipe_item:
        db.session.delete(recipe_item)
        db.session.commit()

    return jsonify(success=True), 200