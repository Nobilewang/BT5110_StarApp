from flask import Flask,jsonify,url_for,redirect,request,render_template
from flask_sqlalchemy import SQLAlchemy
import config
from apps.book import bp as book_bp
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
import psycopg2
from flask import render_template, redirect, request, url_for
from apps.forms import RegisterForm
import pandas as pd


Base = declarative_base()
# HOSTNAME='127.0.0.1'
USERNAME='Gaoda'
PASSWORD='Gaoda'
DATABASE='StarAPP'
DB_URI='postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(USERNAME,PASSWORD,DATABASE)
# engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/db_name'.format(USERNAME,PASSWORD,HOSTNAME,DATABASE))
# db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.register_blueprint(book_bp)
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI']=DB_URI
db = SQLAlchemy(app)

# migrate = Migrate(app,db)

connection = psycopg2.connect(user="Gaoda",
                                      password="Gaoda",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="StarAPP")
cursor = connection.cursor()

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

books=[{"id":1,"name":"yi"},
       {"id":2,"name":"er"},
       {"id":3,"name":"san"},
       {"id":4,"name":"si"}]

@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)
        return redirect('/about')
    return render_template('login.html')

@app.route('/register' ,methods=['GET','POST'])

def register():
    connection = psycopg2.connect(user="Gaoda",
                                  password="Gaoda",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="StarAPP")
    form=RegisterForm(request.form)
    if form.validate():
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)
        cursor = connection.cursor()
        postgreSQL_insert_Query = "INSERT into public.user(username,password) VALUES ('{}','{}')".format(username,password)
        print(postgreSQL_insert_Query)
        cursor.execute(postgreSQL_insert_Query)
        connection.commit()
        return redirect('/login')
    else:
        pass
    return render_template('register.html')

    # username=request.form.get('username')
    # password=request.form.get('password')
    # print(username,password)
    return render_template('register.html')



@app.route('/control')
def control():
    context ={
        "age": 18,
        "books":['ni','gg','a'],
        "person":{'name':'Gaoda','age':23}
    }
    return render_template("control.html", **context)


@app.route('/about')
def about():
    df = pd.DataFrame({'Patient Name': ["Some name", "Another name"],
                       "Patient ID": [123, 456],
                       "Misc Data Point": [8, 53]})
    return render_template("about.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="Patient ID", zip=zip)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    for book in books:
        if book_id==book['id']:
            return book
    return f"{book_id}not matched"
            # return f'{book_id}not matched'

@app.route('/profile')
def profile():
    user_id=request.args.get("id")
    if user_id:
        return "用户个人中心"
    else:
        return redirect(url_for("index"))


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

# @app.route('/db')
# def database():
    # engine = db.get_engine()

    # class User(db.Model):
    #     __tablename__ = 'User_table'
    #     product_id = db.Column(db.String(80), )
    #     store_id = db.Column(db.String(80)，)
    #     id = db.Column(db.Integer, primary_key=True)

    # db.create_all()
    # with engine.connect() as conn:
    #     result=conn.execute ('select 1')
    #     print(result.fetchstone())
    # return 'Hello_World'
    # conn.close()


if __name__ == '__main__':
    app.run()
