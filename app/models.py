from app import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    recipe_item = db.relationship('RecipeItem', backref='item', lazy='dynamic')

    def __repr__(self):
        return '<Item {}>'.format(self.name)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    recipe_item = db.relationship('RecipeItem', backref='recipe', lazy='dynamic')
    recipe_date_log = db.relationship('RecipeDateLog', backref='recipe', lazy='dynamic')

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'))
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'))
    quantity = db.Column(db.Integer, default=1)


class RecipeDateLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'))
    quantity = db.Column(db.Integer, default=1)

