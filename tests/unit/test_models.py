from app.models import Item


def test_new_item(new_item):
    """
    GIVEN am Item model
    WHEN a new item is created
    THEN check the name, quanity and recipe are defined correctly
    """
    assert new_item.name == 'item_name'
    assert new_item.quantity == 1
    assert new_item.recipe == None
