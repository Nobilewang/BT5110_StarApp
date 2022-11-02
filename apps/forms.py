import wtforms
from wtforms.validators import length, email, EqualTo
import psycopg2

class RegisterForm(wtforms.Form):
    username=wtforms.StringField(validators=[length(min=3,max=20)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    confirm_password = wtforms.StringField(validators=[EqualTo("password")])


    def validate_username(self, field):
        connection = psycopg2.connect(user="Gaoda",
                                      password="Gaoda",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="StarAPP")
        cursor = connection.cursor()
        username=field.data
        postgreSQL_select_Query = "select u.username from public.user u where u.username = '{}'".format(username)
        cursor.execute(postgreSQL_select_Query)
        check_result = cursor.fetchall()
        if username == check_result :
            raise wtforms.ValidationError("username existed")
