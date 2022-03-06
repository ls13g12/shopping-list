from flask import render_template, redirect, url_for, jsonify, request
from app import db
from app.models import Item
from app.main import bp


@bp.route('/')
@bp.route('/list')
def list():
    items = Item.query.all()
    return render_template('list.html', items=items)

