from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Required


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class Search(FlaskForm):
    search_item = SelectField(u'Select Category', choices=[('title','Title'),('author','Author'),('isbn','ISBN number')],validators=[Required()])
    name = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')