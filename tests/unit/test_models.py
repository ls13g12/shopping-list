from app.models import Item, Recipe, RecipeItem

def test_new_item(new_item):
    """
    GIVEN an Item model
    WHEN a new item is created
    THEN check the name,
    """
    assert new_item.name == 'item_name'


def test_new_recipe(new_recipe):
    """
    GIVEN a Recipe model
    WHEN a new recipe is created
    THEN check the name,
    """
    assert new_recipe.name == 'recipe_name'

def test_new_recipe_item(new_recipe_item):
    """
    GIVEN a RecipeItem model
    WHEN a new recipe item (junction entry) is created
    THEN check the 
    """

    assert new_recipe_item.quantity == 1

