from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class SelectDatesForm(FlaskForm):
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_dates(self, start_date, end_date):
        if end_date < start_date:
            raise ValidationError("End date must be after start date")
        return True
