import os
basedir = os.path.abspath(os.path.dirname(__file__))
import contextlib
import unittest
from flask import current_app, template_rendered
from app import create_app, db
from app.models import Item, Recipe, RecipeItem

@contextlib.contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'test_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = True


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.populate_db()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_home_page_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'

    def populate_db(self):
        item = Item(name='lasagne sheets')
        item2 = Item(name='tinned tomatoes')
        item3 = Item(name='mince')
        item4 = Item(name='cheese')
        db.session.add_all([item, item2, item3, item4])

        recipe = Recipe(name='lasagne')
        db.session.add(recipe)

        recipe_item=RecipeItem(recipe_id=recipe.id, item_id=item.id, quantity=1)
        recipe_item2=RecipeItem(recipe_id=recipe.id, item_id=item2.id, quantity=1)
        recipe_item3=RecipeItem(recipe_id=recipe.id, item_id=item3.id, quantity=1)
        recipe_item4=RecipeItem(recipe_id=recipe.id, item_id=item4.id, quantity=1)
        db.session.add_all([recipe_item, recipe_item2, recipe_item3, recipe_item4])
        
        db.session.commit()

    def test_home_page_data(self):
        rv=self.client.get('/', follow_redirects=True)
        #nav bar buttons
        assert b'List' in rv.data
        assert b'Recipes' in rv.data
        assert b'Calendar' in rv.data

        with captured_templates(self.app) as templates:
            rv = self.client.get('/')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'list.html'

            




