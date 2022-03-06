import pytest
from app import create_app
from app.models import Item


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture(scope='module')
def new_item():
    item = Item(name='item_name', quantity=1)
    return item

