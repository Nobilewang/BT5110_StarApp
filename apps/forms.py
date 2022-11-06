import wtforms
from wtforms.validators import length, email, EqualTo
import psycopg2

class RegisterForm(wtforms.Form):
    username=wtforms.StringField(validators=[length(min=3,max=20)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    confirm_password = wtforms.StringField(validators=[EqualTo("password")])



