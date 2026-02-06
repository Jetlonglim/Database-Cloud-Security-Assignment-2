from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[
        DataRequired(),
        Length(min=1, max=200),
        Regexp(r'^[a-zA-Z0-9\s\-\!\?]+$', message="Title contains invalid characters")
    ])
    author = StringField('Author', validators=[
        DataRequired(),
        Length(min=3, max=100),
        Regexp(r'^[a-zA-Z ]+$', message="Author name must contain only letters and spaces")
    ])
    isbn = StringField('ISBN', validators=[
        DataRequired(),
        Length(min=10, max=20),
        Regexp(r'^[0-9\-]+$', message="ISBN must contain only numbers and hyphens")
    ])
    submit = SubmitField('Add Book')