from flask import Flask,jsonify,url_for,redirect,request,render_template
# from flask_sqlalchemy import SQLAlchemy
import config
from apps.book import bp as book_bp
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker, relationship
# from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
import psycopg2
from flask import render_template, redirect, request, url_for
from apps.forms import RegisterForm
import pandas as pd
import os
from query import get_date_cache, test, plot_function, QRcode, hierarchy, Store_analysis,promo_analysis,promo_image,h_S_average,promotion_bin_analysis
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# Base = declarative_base()
# HOSTNAME='127.0.0.1'
USERNAME='svzkvuhynjemhg'
PASSWORD='449c5054517dd2e36b0e95a74cf7b111faf82ac1d04b4c9b81a0378ff367790e'
DATABASE='d43n4a0o292kq4'
HOST_N = "ec2-34-194-73-236.compute-1.amazonaws.com"
PORT_N = '5432'
# connection = psycopg2.connect(user=USERNAME,
#                                   password=PASSWORD,
#                                   host=HOST_N,
#                                   port=PORT_N,
#                                   database=DATABASE)
# DB_URI='postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(USERNAME,PASSWORD,DATABASE)
# engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/db_name'.format(USERNAME,PASSWORD,HOSTNAME,DATABASE))
# db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.register_blueprint(book_bp)
app.config.from_object(config)
# app.config['SQLALCHEMY_DATABASE_URI']=DB_URI
# db = SQLAlchemy(app)

# migrate = Migrate(app,db)

# user = os.environ.get('username', 'Gaoda')
# password = os.environ.get('password', 'Gaoda')
# hostname = os.environ.get('hostname', '127.0.0.1')
# port = os.environ.get('port', '5432')
# db = os.environ.get('db', 'StarAPP')

#
# connection = psycopg2.connect(user=user,
#                                       password=password,
#                                       host=hostname,
#                                       port=port,
#                                       database=db)
# connection = psycopg2.connect(user="postgres",
#                               password="123456",
#                               host="127.0.0.1",
#                               port="5432",
#                               database="starapp")
connection = psycopg2.connect(user=USERNAME,
                                  password=PASSWORD,
                                  host=HOST_N,
                                  port=PORT_N,
                                  database=DATABASE)








cursor = connection.cursor()

# from sqlalchemy import create_engine
# sales=pd.read_csv('')
# date=pd.read_csv
# promo_dem=pd.read_csv
# prod=pd.read_csv
# stores=pd.read_csv

# USERNAME='postgres'
# PASSWORD='123456'
# DATABASE='starapp'
# DB_URI='postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(USERNAME,PASSWORD,DATABASE)
# engine = create_engine(DB_URI)
# sales.to_sql('sales', engine)
# date.to_sql('date', engine)
# promo_dem.to_sql('promotion', engine)
# prod.to_sql('products',engine)
# stores.to_sql('stores',engine)

# with engine.connect() as con:
#     con.execute('ALTER TABLE stores ADD PRIMARY KEY (store_id);')
#     con.execute('ALTER TABLE products ADD PRIMARY KEY (product_id);')
#     con.execute('ALTER TABLE "sales" ALTER COLUMN date TYPE date;')
#     con.execute('ALTER TABLE "date" ALTER COLUMN date TYPE date;')
#     con.execute('ALTER TABLE "promotion" ALTER COLUMN date TYPE date;')
#     con.execute('ALTER TABLE promotion ADD PRIMARY KEY (product_id,store_id,date,promo_type_1);')
#     con.execute('ALTER TABLE date ADD PRIMARY KEY (date);')
#     con.execute('ALTER TABLE sales ADD PRIMARY KEY (product_id,store_id,date);')

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
        return redirect('/home')
    return render_template('login.html')

@app.route('/date' ,methods=['GET','POST'])
def date():
    if request.method == 'POST':
        # connection = psycopg2.connect(user="postgres",
        #                               password="123456",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="starapp")
        connection = psycopg2.connect(user=USERNAME,
                                      password=PASSWORD,
                                      host=HOST_N,
                                      port=PORT_N,
                                      database=DATABASE)
        timespan = request.form.get('timespan')
        store = request.form.get('storeid')
        product = request.form.get('productid')
        cursor = connection.cursor()
        postgreSQL_insert_Query = "Delete from cache_time"
        cursor.execute(postgreSQL_insert_Query)
        postgreSQL_insert_Query = "INSERT into cache_time(time,store,product) VALUES ('{}','{}','{}')".format(timespan, store,product)
        cursor.execute(postgreSQL_insert_Query)
        connection.commit()
        return redirect('/date/report')
    return render_template('date.html')

@app.route('/single_date' ,methods=['GET','POST'])
def single_date():
    if request.method == 'POST':
        # connection = psycopg2.connect(user="postgres",
        #                               password="123456",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="starapp")
        connection = psycopg2.connect(user=USERNAME,
                                      password=PASSWORD,
                                      host=HOST_N,
                                      port=PORT_N,
                                      database=DATABASE)
        date_cache = request.form.get('date')
        store = request.form.get('storeid')
        product = request.form.get('productid')
        cursor = connection.cursor()
        postgreSQL_insert_Query = "DELETE FROM cache_time"
        cursor.execute(postgreSQL_insert_Query)
        postgreSQL_insert_Query = "INSERT into cache_time(time,store,product) VALUES ('{}','{}','{}')".format(date_cache, store,product)
        cursor.execute(postgreSQL_insert_Query)
        connection.commit()
        return redirect('/single_date/report')
    return render_template('single_date.html')

@app.route('/register' ,methods=['GET','POST'])

def register():
    # connection = psycopg2.connect(user="postgres",
    #                               password="123456",
    #                               host="127.0.0.1",
    #                               port="5432",
    #                               database="starapp")
    connection = psycopg2.connect(user=USERNAME,
                                  password=PASSWORD,
                                  host=HOST_N,
                                  port=PORT_N,
                                  database=DATABASE)
    form=RegisterForm(request.form)
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)
        cursor = connection.cursor()
        postgreSQL_insert_Query = "INSERT into redisuser(username,password) VALUES ('{}','{}')".format(username,password)
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

@app.route('/date/report')
def date_report():
    result_list = get_date_cache()
    return render_template("control.html", result=result_list)

@app.route('/plot.png')
def plot_png():
    result_list = get_date_cache()
    fig = plot_function(p1=str(result_list[0]),p2= str(result_list[1]),p3=str(result_list[2]))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


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
def welcome():  # put application's code here
    return render_template("welcome.html")

@app.route('/home')
def home():  # put application's code here
    return render_template("index.html")
@app.route('/hich')
def QRcode_view():
    result_list = hierarchy()
    df = QRcode(h=str(result_list[0]))
    df.reset_index(inplace=True)
    names = []
    for i in range(len(df.columns)):
        names.append(df.columns.values[i][0])
    # df = pd.DataFrame({'Patient Name': ["Some name", "Another name"],
    #                    "Patient ID": [123, 456],
    #                    "Misc Data Point": [8, 53]})
    return render_template("hich.html", column_names=names, row_data=list(df.values.tolist()),
                           link_column="hierarchy1", zip=zip)




@app.route('/hich_1' ,methods=['GET','POST'])
def QRcode_search():
    if request.method == 'POST':
        # connection = psycopg2.connect(user="postgres",
        #                               password="123456",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="starapp")
        connection = psycopg2.connect(user=USERNAME,
                                      password=PASSWORD,
                                      host=HOST_N,
                                      port=PORT_N,
                                      database=DATABASE)
        hierarchy = request.form.get('hierarchy')
        cursor = connection.cursor()
        postgreSQL_insert_Query = "Delete from cache_time"
        cursor.execute(postgreSQL_insert_Query)
        postgreSQL_insert_Query = "INSERT into cache_time(time,store,product) VALUES ('{}','0','0')".format(hierarchy)
        cursor.execute(postgreSQL_insert_Query)
        connection.commit()
        return redirect('/hich')
    return render_template('hich_1.html')

@app.route('/stores')
def store_view():

    df = Store_analysis()
    # df.reset_index(inplace=True)
    # names = []
    # for i in range(len(df.columns)):
    #     names.append(df.columns.values[i][0])
    # df = pd.DataFrame({'Patient Name': ["Some name", "Another name"],
    #                    "Patient ID": [123, 456],
    #                    "Misc Data Point": [8, 53]})
    return render_template("store.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="hierarchy1", zip=zip)




@app.route('/promo')
def promo_table():

    promo_frame, fig1, fig2, fig3, fig4, fig5, fig6  = promo_analysis()
    # df.reset_index(inplace=True)
    names = []
    for i in range(len(promo_frame.columns)):
        names.append(promo_frame.columns.values[i][0])
    # df = pd.DataFrame({'Patient Name': ["Some name", "Another name"],
    #                    "Patient ID": [123, 456],
    #                    "Misc Data Point": [8, 53]})
    return render_template("promo.html", column_names=names, row_data=list(promo_frame.values.tolist()),
                           link_column="hierarchy1", zip=zip)


@app.route('/plot1.png')
def promo_image_view():
    result_list = promo_image()
    promo_frame, fig1, fig2, fig3, fig4, fig5, fig6 = promo_analysis()
    if result_list[0][:5] == 'S0002':
        output = io.BytesIO()
        FigureCanvas(fig1).print_png(output)
    elif result_list[0][:5] == 'S0012':
        output = io.BytesIO()
        FigureCanvas(fig2).print_png(output)
    elif result_list[0][:5] == 'S0013':
        output = io.BytesIO()
        FigureCanvas(fig3).print_png(output)
    elif result_list[0][:5] == 'S0023':
        output = io.BytesIO()
        FigureCanvas(fig4).print_png(output)
    elif result_list[0][:5] == 'S0040':
        output = io.BytesIO()
        FigureCanvas(fig5).print_png(output)
    elif result_list[0][:5] == 'S0050':
        output = io.BytesIO()
        FigureCanvas(fig6).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')


@app.route('/promo' ,methods=['GET','POST'])
def promo_search():
    if request.method == 'POST':
        # connection = psycopg2.connect(user="postgres",
        #                               password="123456",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="starapp")
        connection = psycopg2.connect(user=USERNAME,
                                      password=PASSWORD,
                                      host=HOST_N,
                                      port=PORT_N,
                                      database=DATABASE)

        promop = request.form.get('productid')
        cursor = connection.cursor()
        postgreSQL_insert_Query = "Delete from cache_time"
        cursor.execute(postgreSQL_insert_Query)
        postgreSQL_insert_Query = "INSERT into cache_time(time,store,product) VALUES ('{}','0','0')".format(promop)
        cursor.execute(postgreSQL_insert_Query)
        connection.commit()
        return redirect('/ppp')
    return render_template('promo.html')

@app.route('/ppp')
def promo_report():
    result_list = promo_image()
    return render_template("promoimage1.html", result=result_list)




@app.route('/knock_e')
def knock_table():

    promo_ana,df1,df2 = h_S_average()
    # df.reset_index(inplace=True)
    names = []
    for i in range(len(promo_ana.columns)):
        names.append(promo_ana.columns.values[i][0])
    # df = pd.DataFrame({'Patient Name': ["Some name", "Another name"],
    #                    "Patient ID": [123, 456],
    #                    "Misc Data Point": [8, 53]})
    return render_template("knock_e.html", column_names=names, row_data=list(promo_ana.values.tolist()),
                           link_column="hierarchy1", zip=zip)



@app.route('/plotk1.png')
def knock_image_view1():
    promo_ana,df1,df2 = h_S_average()
    output = io.BytesIO()
    FigureCanvas(df1).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plotk2.png')
def knock_image_view2():
    promo_ana,df1,df2 = h_S_average()
    output = io.BytesIO()
    FigureCanvas(df2).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')


@app.route('/promotion/bin')
def promo_bin():
    return render_template("promotion_bin.html")
@app.route('/plotpmavg.png')
def plot_pngavg():
    fig_avg_total,fig_diff,fig_cleaned = promotion_bin_analysis()
    # fig = plot_function(p1=str(result_list[0]),p2= str(result_list[1]),p3=str(result_list[2]))
    output = io.BytesIO()
    FigureCanvas(fig_avg_total).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plotpmbin.png')
def plot_pngbin():
    fig_avg_total,fig_diff,fig_cleaned = promotion_bin_analysis()
    # fig = plot_function(p1=str(result_list[0]),p2= str(result_list[1]),p3=str(result_list[2]))
    output = io.BytesIO()
    FigureCanvas(fig_diff).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plotpmbinclean.png')
def plot_pngbinclean():
    fig_avg_total,fig_diff,fig_cleaned = promotion_bin_analysis()
    # fig = plot_function(p1=str(result_list[0]),p2= str(result_list[1]),p3=str(result_list[2]))
    output = io.BytesIO()
    FigureCanvas(fig_cleaned).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/single_date/report')
def single_date_report():
    result_list = get_date_cache()
    result_single_day = plot_function( check_single_date=str(result_list[0]),p2= str(result_list[1]),p3=str(result_list[2]))
    print(result_single_day)
    return render_template("single_date_report.html" , result=result_single_day)

if __name__ == '__main__':
    app.run()
