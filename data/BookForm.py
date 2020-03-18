from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    fio = SelectField('Автор', coerce=int, validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    genres = SelectMultipleField('Жанры', coerce=int)
    submit = SubmitField('Сохранить')
