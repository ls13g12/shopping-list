from app import db
from app.api import bp
from app.models import SelectedDatesLog
from flask import make_response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


@bp.route("/api/selecteddates", methods=["GET"])
def get_selected_dates():
    try:
        dates = SelectedDatesLog.query.order_by(
            SelectedDatesLog.timestamp.desc()
        ).first()
        if dates:
            dates = {
                "start_date": dates.start_date.strftime("%m/%d/%Y"),
                "end_date": dates.end_date.strftime("%m/%d/%Y"),
            }
        res = make_response(jsonify({"dates": dates}), 200)
        return res

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        res = make_response(jsonify({"error": error}), 500)
        return res


@bp.route("/api/selecteddates", methods=["PUT"])
def update_selected_dates():
    # lower case recipe name from fetch request body
    req = request.get_json()
    start_date = req["start_date"]
    end_date = req["end_date"]
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    try:
        selected_dates = SelectedDatesLog.query.first()
        selected_dates.start_date = start_date
        selected_dates.end_date = end_date
        selected_dates.timestamp = datetime.now()
        db.session.commit()

        res = make_response(jsonify({}), 204)
        return res

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        res = make_response(jsonify({"error": error}), 500)
        return res
