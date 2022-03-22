import pytest
from app import create_app
from app.models import Item, Recipe, RecipeItem


@pytest.fixture()
def app():
    app = create_app()
    return app

@pytest.fixture(scope='module')
def new_item():
    item = Item(name='item_name')
    return item

@pytest.fixture(scope='module')
def new_recipe():
    recipe = Recipe(name='recipe_name')
    return recipe

@pytest.fixture(scope='module')
def new_recipe_item():
    item = Item(name='item_name')
    recipe = Recipe(name='recipe_name')
    recipe_item = RecipeItem(item_id=item.id, recipe_id=recipe.id, quantity=1)
    return recipe_item


