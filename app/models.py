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

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'))
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'))
    quantity = db.Column(db.Integer, default=1)



'''

class Item_Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)



class Weekday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    recipes = db.relationship('Recipe', backref='weekday', lazy='dynamic')

    def __repr__(self):
        return '<Weekday {}>'.format(self.name)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    passcode_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

'''
