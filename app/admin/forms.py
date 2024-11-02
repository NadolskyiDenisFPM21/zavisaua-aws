from wtforms.fields.simple import StringField, PasswordField
from wtforms.form import Form
from wtforms.validators import DataRequired, Email


class UserAdminForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])