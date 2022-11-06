import os.path

import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
import sys
import pandas as pd
import seaborn
import scipy.stats as stats

USERNAME='svzkvuhynjemhg'
PASSWORD='449c5054517dd2e36b0e95a74cf7b111faf82ac1d04b4c9b81a0378ff367790e'
DATABASE='d43n4a0o292kq4'
HOST_N = "ec2-34-194-73-236.compute-1.amazonaws.com"
PORT_N = '5432'


def get_date_cache():
        result_list=[]
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
        postgreSQL_select_Query = "select p.time from cache_time p LIMIT 1"
        cursor.execute(postgreSQL_select_Query)
        time = cursor.fetchall()
        time=time[0]
        time = time[0]


        postgreSQL_select_Query = "select p.store from cache_time p LIMIT 1"
        cursor.execute(postgreSQL_select_Query)
        store = cursor.fetchall()
        store = store[0]
        store = store[0][:5]
        if "S" not in store:
            store = 'na'

        postgreSQL_select_Query = "select p.product from cache_time p LIMIT 1"
        cursor.execute(postgreSQL_select_Query)
        product = cursor.fetchall()
        product = product[0]
        product=product[0][:5]
        if "P" not in product:
            product = 'na'


        result_list.append(time)
        result_list.append(store)
        result_list.append(product)

        return result_list

get_date_cache()

def test(p1,p2,p3):
    return [p1,p2,p3]


def plot_function(p1='na', p2='na', p3='na', check_single_date='no'):
    postgreSQL_select_Query = 0
    if p1 == 'na' and p2 == 'na' and p3 == 'na' and check_single_date == 'no':
        print('Null value of the date blank is not acceptable!!!')
    else:

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

        if p1 != 'na' and p2 == 'na' and p3 == 'na' and check_single_date == 'no':
            postgreSQL_select_Query = 'select AVG(s.revenue) as "Average Revenue", d.{} from sales s, date d where d.date = s.date group by d.{} order by d.{}'.format(
                p1, p1, p1)
        elif p1 != 'na' and p2 != 'na' and p3 == 'na' and check_single_date == 'no':
            postgreSQL_select_Query = "select AVG(s.revenue), d.{} from sales s, date d where d.date = s.date AND s.store_id = '{}' group by d.{} order by d.{}".format(
                p1, p2, p1, p1)
        elif p1 != 'na' and p3 != 'na' and p2 == 'na' and check_single_date == 'no':
            postgreSQL_select_Query = "select AVG(s.revenue), d.{} from sales s, date d where d.date = s.date AND s.product_id = '{}' group by d.{} order by d.{}".format(
                p1, p3, p1, p1)
        elif p1 != 'na' and p2 != 'na' and p3 != 'na' and check_single_date == 'no':
            postgreSQL_select_Query = "select AVG(s.revenue), d.{} from sales s, date d where d.date = s.date AND s.product_id = '{}' AND s.store_id = '{}' group by d.{} order by d.{}".format(
                p1, p3, p2, p1, p1)
        elif p1 == 'na' and p2 == 'na' and p3 == 'na' and check_single_date != 'no':
            postgreSQL_select_Query = "select AVG(s.revenue) from sales s, date d where d.date = '{}'".format(
                check_single_date)
        elif p1 == 'na' and p2 != 'na' and p3 == 'na' and check_single_date != 'no':
            postgreSQL_select_Query = "select AVG(s.revenue) from sales s, date d where d.date = '{}' AND s.store_id = '{}'".format(
                check_single_date, p2)
        elif p1 == 'na' and p2 == 'na' and p3 != 'na' and check_single_date != 'no':
            postgreSQL_select_Query = "select AVG(s.revenue) from sales s, date d where d.date = '{}' AND s.product_id = '{}'".format(
                check_single_date, p3)
        elif p1 == 'na' and p2 != 'na' and p3 != 'na' and check_single_date != 'no':
            postgreSQL_select_Query = "select AVG(s.revenue) from sales s, date d where d.date = '{}' AND s.product_id = '{}' AND s.store_id = '{}'".format(
                check_single_date, p3, p2)
        if postgreSQL_select_Query == 0:
            print('wrong input parameters')
        else:
            # print(postgreSQL_select_Query)
            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()

            if len(mobile_records) == 1:
                print(mobile_records[0][0])
                result_single_day = mobile_records[0][0]
                return result_single_day
            else:
                plot_df = pd.DataFrame(mobile_records, columns=['Average Revenue', 'datetype'])

                if p1 == 'date':
                    fig = plt.figure()
                    plt.plot(plot_df['datetype'], plot_df['Average Revenue'])
                    plt.show()
                    print(1)
                    return fig
                    # fig.savefig('timespan.png')


                else:
                    fig = plt.figure()
                    plt.plot(plot_df['datetype'], plot_df['Average Revenue'], 'g*-')
                    for a, b in zip(plot_df['datetype'], np.round(np.array(plot_df['Average Revenue']), 2)):
                        plt.text(a, b + 0.001, '%.2f' % b, ha='center', va='bottom', fontsize=9)
                    plt.show()
                    return fig
                    # fig.savefig('timespan.png')


plot_function(p1='month',p2='na',p3='na')

def QRcode(h='hierarchy1_id'):
    if h == 0:
        print('wrong input')

    elif h =='hierarchy1_id' or 'hierarchy2_id':
        # connection = psycopg2.connect(user="postgres",
        #                           password="123456",
        #                           host="127.0.0.1",
        #                           port="5432",
        #                           database="starapp")
        connection = psycopg2.connect(user=USERNAME,
                                      password=PASSWORD,
                                      host=HOST_N,
                                      port=PORT_N,
                                      database=DATABASE)

        cursor = connection.cursor()
        # postgreSQL_select_Query = "select * from sales s, products p where p.product_id = s.product_id"
        postgreSQL_select_Query = "select SUM(s.sales) Total_sales, SUM(s.revenue) Total_revenue, p.{} from sales s, products p where p.product_id = s.product_id group by p.{}".format(h,h)
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        mobile_records = pd.DataFrame(mobile_records)
        mobile_records.columns = [['Total_sales','Total_revenue','hierarchy']]
        mobile_records.index = mobile_records['hierarchy'].values.squeeze()
        mobile_records = mobile_records.rename_axis('hierarchy').drop(columns=['hierarchy'])
    return mobile_records


def hierarchy():
        result_list=[]
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
        postgreSQL_select_Query = "select p.time from cache_time p LIMIT 1"
        cursor.execute(postgreSQL_select_Query)
        time = cursor.fetchall()
        time=time[0]
        time = time[0]

        result_list.append(time)

        return result_list


def promo_image():
    result_list = []
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
    postgreSQL_select_Query = "select p.time from cache_time p LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    time = cursor.fetchall()
    time = time[0]
    time = time[0]

    result_list.append(time)

    return result_list






def Store_analysis():
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
    postgreSQL_select_Query = 'select st.store_id, st.store_size, st.city_id , sum(s.revenue) as "Total Revenue", sum(s.sales) as "Total Sales" from sales s, stores st where st.store_id = s.store_id Group by  st.store_id, st.store_size, st.city_id order by st.store_size ASC'
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    store_records = pd.DataFrame(store_records).rename(
        columns={0: 'Store_ID', 1: 'Store_Size', 2: 'City_ID', 3: 'Total_Revenue', 4: 'Total_Sales'})

    return store_records


def promo_analysis():
    promo_frame = pd.DataFrame()
    Product_ID = []
    baseline_ave_sales = []
    N_sales_f_ba_p = []
    N_sales_f_d_p = []
    N_sales_f_promo = []
    promo_type = []
    promo_frame = pd.DataFrame()

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

    ####### P0051, pr03, S0002

    # average sale
    postgreSQL_select_Query = "select avg(s.sales) avereage_sale from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR14' "
    cursor.execute(postgreSQL_select_Query)
    average_sales = pd.DataFrame(cursor.fetchall())
    ## promo12_analysis
    postgreSQL_select_Query2 = "select s.sales from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp)::date - INTERVAL '7 day' and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp)::date + INTERVAL '7 day'"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Query2 = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp)"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis_promo = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Querybefore = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp)::date - INTERVAL '7 day' and s.date < (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp) "
    cursor.execute(postgreSQL_select_Querybefore)
    promo12_analysis_before = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Queryafter = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.date > (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0051' and s.store_id = 'S0002' and s.promo_type_1 = 'PR03') as temp)::date + INTERVAL '7 day' "
    cursor.execute(postgreSQL_select_Queryafter)
    promo12_analysis_after = pd.DataFrame(cursor.fetchall())

    promo_not_promo_loss = -average_sales * 14 + promo12_analysis_before + promo12_analysis_after
    promo_in_promo_loss = -average_sales * 14 + promo12_analysis_promo

    Product_ID.append('P0051')
    promo_type.append('PR03')
    baseline_ave_sales.append(average_sales.iloc[0, 0])
    N_sales_f_ba_p.append(promo_not_promo_loss.iloc[0, 0])
    N_sales_f_d_p.append(promo_in_promo_loss.iloc[0, 0])
    N_sales_f_promo.append(promo_in_promo_loss.iloc[0, 0] + promo_not_promo_loss.iloc[0, 0])

    fig1 = plt.figure()
    plt.plot(promo12_analysis.index, promo12_analysis[0])
    plt.axhline(y=average_sales.values, color='green', linestyle='--', lw=2)
    plt.axvline(x=7, color='r', linestyle='--', lw=2)
    plt.axvline(x=20, color='r', linestyle='--', lw=2)
    # plt.show()

    ### S0012; P0129, PR05

    # average sale
    postgreSQL_select_Query = "select avg(s.sales) avereage_sale from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR14' "
    cursor.execute(postgreSQL_select_Query)
    average_sales = pd.DataFrame(cursor.fetchall())

    ## promo12_analysis
    postgreSQL_select_Query2 = "select s.sales from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp)::date - INTERVAL '2 day' and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp)::date + INTERVAL '3 day'"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Query2 = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp)"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis_promo = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Querybefore = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp)::date - INTERVAL '2 day' and s.date < (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp) "
    cursor.execute(postgreSQL_select_Querybefore)
    promo12_analysis_before = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Queryafter = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.date > (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0012' and s.promo_type_1 = 'PR05') as temp)::date + INTERVAL '3 day' "
    cursor.execute(postgreSQL_select_Queryafter)
    promo12_analysis_after = pd.DataFrame(cursor.fetchall())

    promo_not_promo_loss = -average_sales * 4 + promo12_analysis_before + promo12_analysis_after
    promo_in_promo_loss = -average_sales * 4 + promo12_analysis_promo

    Product_ID.append('P0129')
    promo_type.append('PR05')
    baseline_ave_sales.append(average_sales.iloc[0, 0])
    N_sales_f_ba_p.append(promo_not_promo_loss.iloc[0, 0])
    N_sales_f_d_p.append(promo_in_promo_loss.iloc[0, 0])
    N_sales_f_promo.append(promo_in_promo_loss.iloc[0, 0] + promo_not_promo_loss.iloc[0, 0])

    fig2 = plt.figure()
    plt.plot(promo12_analysis.index, promo12_analysis[0])
    plt.axhline(y=average_sales.values, color='green', linestyle='--', lw=2)
    plt.axvline(x=2, color='r', linestyle='--', lw=2)
    plt.axvline(x=5, color='r', linestyle='--', lw=2)
    # plt.show()

    ### S0013; P0261 PR10

    # average sale
    postgreSQL_select_Query = "select avg(s.sales) avereage_sale from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.promo_type_1 = 'PR14' "
    cursor.execute(postgreSQL_select_Query)
    average_sales = pd.DataFrame(cursor.fetchall())

    ## promo12_analysis
    postgreSQL_select_Query2 = "select s.sales from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp)::date - INTERVAL '7 day' and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp)::date + INTERVAL '7 day'"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Query2 = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp)"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis_promo = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Querybefore = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp)::date - INTERVAL '7 day' and s.date < (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp) "
    cursor.execute(postgreSQL_select_Querybefore)
    promo12_analysis_before = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Queryafter = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date > (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0261' and s.store_id = 'S0013' and s.date >= '2017-06-15' and s.date <= '2017-06-28') as temp)::date + INTERVAL '3 day' "
    cursor.execute(postgreSQL_select_Queryafter)
    promo12_analysis_after = pd.DataFrame(cursor.fetchall())

    promo_not_promo_loss = -average_sales * 14 + promo12_analysis_before + promo12_analysis_after
    promo_in_promo_loss = -average_sales * 14 + promo12_analysis_promo

    Product_ID.append('P0261')
    promo_type.append('PR10')
    baseline_ave_sales.append(average_sales.iloc[0, 0])
    N_sales_f_ba_p.append(promo_not_promo_loss.iloc[0, 0])
    N_sales_f_d_p.append(promo_in_promo_loss.iloc[0, 0])
    N_sales_f_promo.append(promo_in_promo_loss.iloc[0, 0] + promo_not_promo_loss.iloc[0, 0])

    fig3 = plt.figure()
    plt.plot(promo12_analysis.index, promo12_analysis[0])
    plt.axhline(y=average_sales.values, color='green', linestyle='--', lw=2)
    plt.axvline(x=7, color='r', linestyle='--', lw=2)
    plt.axvline(x=20, color='r', linestyle='--', lw=2)
    # plt.show()

    ### S0023; P0129

    # average sale
    postgreSQL_select_Query = "select avg(s.sales) avereage_sale from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR14' "
    cursor.execute(postgreSQL_select_Query)
    average_sales = pd.DataFrame(cursor.fetchall())

    ## promo12_analysis
    postgreSQL_select_Query2 = "select s.sales from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp)::date - INTERVAL '2 day' and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp)::date + INTERVAL '2 day'"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Query2 = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp)"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis_promo = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Querybefore = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp)::date - INTERVAL '2 day' and s.date < (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp) "
    cursor.execute(postgreSQL_select_Querybefore)
    promo12_analysis_before = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Queryafter = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.date > (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0129' and s.store_id = 'S0023' and s.promo_type_1 = 'PR05') as temp)::date + INTERVAL '2 day' "
    cursor.execute(postgreSQL_select_Queryafter)
    promo12_analysis_after = pd.DataFrame(cursor.fetchall())

    promo_not_promo_loss = -average_sales * 4 + promo12_analysis_before + promo12_analysis_after
    promo_in_promo_loss = -average_sales * 4 + promo12_analysis_promo

    Product_ID.append('P0129')
    promo_type.append('PR05')
    baseline_ave_sales.append(average_sales.iloc[0, 0])
    N_sales_f_ba_p.append(promo_not_promo_loss.iloc[0, 0])
    N_sales_f_d_p.append(promo_in_promo_loss.iloc[0, 0])
    N_sales_f_promo.append(promo_in_promo_loss.iloc[0, 0] + promo_not_promo_loss.iloc[0, 0])

    fig4 = plt.figure()
    plt.plot(promo12_analysis.index, promo12_analysis[0])
    plt.axhline(y=average_sales.values, color='green', linestyle='--', lw=2)
    plt.axvline(x=2, color='r', linestyle='--', lw=2)
    plt.axvline(x=5, color='r', linestyle='--', lw=2)
    # plt.show()

    ### S0040; P0565 pr07

    # average sale
    postgreSQL_select_Query = "select avg(s.sales) avereage_sale from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.promo_type_1 = 'PR14' "
    cursor.execute(postgreSQL_select_Query)
    average_sales = pd.DataFrame(cursor.fetchall())

    ## promo12_analysis
    postgreSQL_select_Query2 = "select s.sales from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp)::date - INTERVAL '7 day' and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp)::date + INTERVAL '11 day'"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Query2 = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp)"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis_promo = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Querybefore = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp)::date - INTERVAL '7 day' and s.date < (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp) "
    cursor.execute(postgreSQL_select_Querybefore)
    promo12_analysis_before = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Queryafter = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date > (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0565' and s.store_id = 'S0040' and s.date >= '2017-09-01' and s.date <= '2017-09-29') as temp)::date + INTERVAL '11 day' "
    cursor.execute(postgreSQL_select_Queryafter)
    promo12_analysis_after = pd.DataFrame(cursor.fetchall())

    promo_not_promo_loss = -average_sales * 14 + promo12_analysis_before + promo12_analysis_after
    promo_in_promo_loss = -average_sales * 29 + promo12_analysis_promo

    Product_ID.append('P0565')
    promo_type.append('PR07')
    baseline_ave_sales.append(average_sales.iloc[0, 0])
    N_sales_f_ba_p.append(promo_not_promo_loss.iloc[0, 0])
    N_sales_f_d_p.append(promo_in_promo_loss.iloc[0, 0])
    N_sales_f_promo.append(promo_in_promo_loss.iloc[0, 0] + promo_not_promo_loss.iloc[0, 0])

    fig5 = plt.figure()
    plt.plot(promo12_analysis.index, promo12_analysis[0])
    plt.axhline(y=average_sales.values, color='green', linestyle='--', lw=2)
    plt.axvline(x=7, color='r', linestyle='--', lw=2)
    plt.axvline(x=35, color='r', linestyle='--', lw=2)
    # plt.show()

    ### S0050; P0689

    # average sale
    postgreSQL_select_Query = "select avg(s.sales) avereage_sale from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.promo_type_1 = 'PR14' "
    cursor.execute(postgreSQL_select_Query)
    average_sales = pd.DataFrame(cursor.fetchall())

    ## promo12_analysis
    postgreSQL_select_Query2 = "select s.sales from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0040' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp)::date - INTERVAL '3 day' and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp)::date + INTERVAL '3 day'"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Query2 = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0040' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp)"
    cursor.execute(postgreSQL_select_Query2)
    promo12_analysis_promo = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Querybefore = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0040' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp)::date - INTERVAL '3 day' and s.date < (select mindate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp) "
    cursor.execute(postgreSQL_select_Querybefore)
    promo12_analysis_before = pd.DataFrame(cursor.fetchall())

    postgreSQL_select_Queryafter = "select sum(s.sales) from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date > (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0040' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp) and s.date <= (select maxdate from (select max(s.date) maxdate ,min(s.date) mindate from sales s , promo p where s.promo_type_1 = p.promo_type_1 and s.product_id = p.product_id and s.store_id = p.store_id and s.date = p.date and s.product_id = 'P0689' and s.store_id = 'S0050' and s.date >= '2017-02-08' and s.date <= '2017-02-13') as temp)::date + INTERVAL '3 day' "
    cursor.execute(postgreSQL_select_Queryafter)
    promo12_analysis_after = pd.DataFrame(cursor.fetchall())

    promo_not_promo_loss = -average_sales * 6 + promo12_analysis_before + promo12_analysis_after
    promo_in_promo_loss = -average_sales * 6 + promo12_analysis_promo

    Product_ID.append('P0689')
    promo_type.append('PR08')
    baseline_ave_sales.append(average_sales.iloc[0, 0])
    N_sales_f_ba_p.append(promo_not_promo_loss.iloc[0, 0])
    N_sales_f_d_p.append(promo_in_promo_loss.iloc[0, 0])
    N_sales_f_promo.append(promo_in_promo_loss.iloc[0, 0] + promo_not_promo_loss.iloc[0, 0])

    fig6 = plt.figure()
    plt.plot(promo12_analysis.index, promo12_analysis[0])
    plt.axhline(y=average_sales.values, color='green', linestyle='--', lw=2)
    plt.axvline(x=3, color='r', linestyle='--', lw=2)
    plt.axvline(x=8, color='r', linestyle='--', lw=2)
    # plt.show()

    promo_frame = pd.concat([pd.DataFrame(Product_ID), pd.DataFrame(baseline_ave_sales), pd.DataFrame(N_sales_f_ba_p),
                             pd.DataFrame(N_sales_f_d_p), pd.DataFrame(N_sales_f_promo), pd.DataFrame(promo_type)],
                            axis=1)
    promo_frame.columns = [['Product ID', 'baseline average sales', 'Sales fluctuation before & after promotion',
                            'Sales fluctuation during promotion', 'Net Sales fluctuation of promotion',
                            'Promotion Type']]
    return promo_frame, fig1, fig2, fig3, fig4, fig5, fig6


promo_frame, fig1, fig2, fig3, fig4, fig5, fig6  = promo_analysis()


def h_S_average():
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
    postgreSQL_select_Query = 'select * from sales , products where sales.product_id = products.product_id'
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    store_records = pd.DataFrame(store_records)
    store_records = store_records.rename(
        columns={1: 'product_id', 2: 'store_id', 3: 'date', 4: 'sales', 5: 'revenue', 6: 'stock', 7: 'price',
                 8: 'promo_type_1', 14: 'hierarchy1_id', 15: 'hierarchy2_id'})
    dff = store_records[
        ['product_id', 'store_id', 'date', 'sales', 'revenue', 'stock', 'price', 'promo_type_1', 'hierarchy1_id',
         'hierarchy2_id']]

    hierarchy = []
    selected_p_norm_average_sale = []
    selected_p_promo_average_sale = []
    other_p_in_same_h_norm_average_sale = []
    other_p_in_same_h_promo_average_sale = []

    ## H01

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H01' and sales.promo_type_1 != 'PR14' and sales.product_id='P0046'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffP1_average_sales = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H01' and sales.promo_type_1 = 'PR14' and sales.product_id='P0046'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffP1_norm_as = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H01' and sales.date in (select * from (select sales.date from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H01' and sales.promo_type_1 != 'PR14' and sales.product_id='P0046') as temp) and sales.promo_type_1 = 'PR14'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffother_average_sales = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H01' and sales.date not in (select * from (select sales.date from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H01' and sales.promo_type_1 != 'PR14' and sales.product_id='P0046') as temp) and sales.promo_type_1 = 'PR14'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffothernot_average_sales = pd.DataFrame(store_records)

    hierarchy.append('H01')
    selected_p_norm_average_sale.append(dffP1_norm_as.iloc[0, 0])
    selected_p_promo_average_sale.append(dffP1_average_sales.iloc[0, 0])
    other_p_in_same_h_norm_average_sale.append(dffothernot_average_sales.iloc[0, 0])
    other_p_in_same_h_promo_average_sale.append(dffother_average_sales.iloc[0, 0])

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H03' and sales.promo_type_1 != 'PR14' and sales.product_id='P0737'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffP1_average_sales = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H03' and sales.promo_type_1 = 'PR14' and sales.product_id='P0737'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffP1_norm_as = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H03' and sales.date in (select * from (select sales.date from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H03' and sales.promo_type_1 != 'PR14' and sales.product_id='P0737') as temp) and sales.promo_type_1 = 'PR14'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffother_average_sales = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H03' and sales.date not in (select * from (select sales.date from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H03' and sales.promo_type_1 != 'PR14' and sales.product_id='P0737') as temp) and sales.promo_type_1 = 'PR14'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffothernot_average_sales = pd.DataFrame(store_records)

    hierarchy.append('H02')
    selected_p_norm_average_sale.append(dffP1_norm_as.iloc[0, 0])
    selected_p_promo_average_sale.append(dffP1_average_sales.iloc[0, 0])
    other_p_in_same_h_norm_average_sale.append(dffothernot_average_sales.iloc[0, 0])
    other_p_in_same_h_promo_average_sale.append(dffother_average_sales.iloc[0, 0])

    ## H00

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H00' and sales.promo_type_1 != 'PR14' and sales.product_id='P0015'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffP1_average_sales = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H00' and sales.promo_type_1 = 'PR14' and sales.product_id='P0015'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffP1_norm_as = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H00' and sales.date in (select * from (select sales.date from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H00' and sales.promo_type_1 != 'PR14' and sales.product_id='P0015') as temp) and sales.promo_type_1 = 'PR14'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffother_average_sales = pd.DataFrame(store_records)

    postgreSQL_select_Query = "select avg(sales.sales) from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H00' and sales.date not in (select * from (select sales.date from sales , products where sales.product_id = products.product_id and products.hierarchy1_id= 'H00' and sales.promo_type_1 != 'PR14' and sales.product_id='P0015') as temp) and sales.promo_type_1 = 'PR14'"
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    dffothernot_average_sales = pd.DataFrame(store_records)

    hierarchy.append('H00')
    selected_p_norm_average_sale.append(dffP1_norm_as.iloc[0, 0])
    selected_p_promo_average_sale.append(dffP1_average_sales.iloc[0, 0])
    other_p_in_same_h_norm_average_sale.append(dffothernot_average_sales.iloc[0, 0])
    other_p_in_same_h_promo_average_sale.append(dffother_average_sales.iloc[0, 0])

    promo_ana = pd.concat([pd.DataFrame(hierarchy), pd.DataFrame(selected_p_norm_average_sale),
                           pd.DataFrame(selected_p_promo_average_sale),
                           pd.DataFrame(other_p_in_same_h_norm_average_sale),
                           pd.DataFrame(other_p_in_same_h_promo_average_sale)], axis=1)
    promo_ana.columns = [['hierarchy1', 'average_sales_of_selected_product_not_in_promo_period',
                          'average_sales_of_selected_product_in_promo_period',
                          'average_sale_of_other_products_not_in_selected_product_promo_period',
                          'average_sale_of_other_products_in_selected_product_promo_period']]

    index = ['H01', 'H02', 'H00']
    df1 = pd.DataFrame({'AS_of_selected_product_not_in_promo': selected_p_norm_average_sale,
                        'AS_of_selected_product_in_promo': selected_p_promo_average_sale}, index=index)
    df1.reset_index(inplace=True)
    df1.columns = ['hierarchy1D', 'AS_of_other_products_not_in_selected_promo',
                   'AS_of_other_products_in_selected_promo']

    fig_kn1 = plt.figure()

    ax = seaborn.barplot(data=df1.melt(id_vars='hierarchy1D',
                                       value_name='score', var_name='in_promo_or_not'),
                         x='hierarchy1D', y='score', hue='in_promo_or_not')

    index = ['H01', 'H02', 'H00']
    df2 = pd.DataFrame({'AS_of_other_products_not_in_selected_promo': other_p_in_same_h_norm_average_sale,
                        'AS_of_other_products_in_selected_promo': other_p_in_same_h_promo_average_sale}, index=index)
    df2.reset_index(inplace=True)
    df2.columns=['hierarchy1D','AS_of_other_products_not_in_selected_promo','AS_of_other_products_in_selected_promo']
    fig_kn2 = plt.figure()

    ax2 = seaborn.barplot(data=df2.melt(id_vars='hierarchy1D',
                                       value_name='score', var_name='in_promo_or_not'),
                         x='hierarchy1D', y='score', hue='in_promo_or_not')

    return promo_ana, fig_kn1, fig_kn2

promo_ana,df1,df2 = h_S_average()






def promotion_bin_analysis():
#Cannibalization Analysis
    # connection = psycopg2.connect(user="Gaoda",
    #                               password="Gaoda",
    #                               host="127.0.0.1",
    #                               port="5432",
    #                               database="StarAPP")

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
    Promotion_Effect_List=[]
    Promotion_Effect_List_cleaned=[]
    Avg_Sales_With_Promotion_List=[]
    Avg_Baseline_Sales_List=[]
    Promotion_Bin_Tier_List=['VERY_LOW','LOW','MODERATE','HIGH','VERYHIGH']
    # PM14
    postgreSQL_select_Query_PM14 = "select s.product_id, avg (s.sales), p.promo_bin_1 from sales s , promo p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type_1 and p.promo_bin_1 = 'NO_RECORD' GROUP by s.product_id,  p.promo_bin_1"
    #verylow
    postgreSQL_select_Query_verylow = "select s.product_id, avg (s.sales), p.promo_bin_1 from sales s , promo p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type_1 and p.promo_bin_1 = 'verylow' GROUP by s.product_id,  p.promo_bin_1"
    # low
    postgreSQL_select_Query_low = "select s.product_id, avg (s.sales), p.promo_bin_1 from sales s , promo p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type_1 and p.promo_bin_1 = 'low' GROUP by s.product_id,  p.promo_bin_1"
    # moderate
    postgreSQL_select_Query_moderate = "select s.product_id, avg (s.sales), p.promo_bin_1 from sales s , promo p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type_1 and p.promo_bin_1 = 'moderate' GROUP by s.product_id,  p.promo_bin_1"
    # high
    postgreSQL_select_Query_high = "select s.product_id, avg (s.sales), p.promo_bin_1 from sales s , promo p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type_1 and p.promo_bin_1 = 'high' GROUP by s.product_id,  p.promo_bin_1"
    # veryhigh
    postgreSQL_select_Query_veryhigh = "select s.product_id, avg (s.sales), p.promo_bin_1 from sales s , promo p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type_1 and p.promo_bin_1 = 'veryhigh' GROUP by s.product_id,  p.promo_bin_1"

    cursor.execute(postgreSQL_select_Query_PM14)
    avgsales_record_pm14 = cursor.fetchall()
    avgsales_record_pm14 = pd.DataFrame(avgsales_record_pm14).rename(columns={0: 'Product_ID', 1: 'Avg_Sales', 2: 'Promo_Bin'})

    cursor.execute(postgreSQL_select_Query_verylow)
    avgsales_record_verylow = cursor.fetchall()
    avgsales_record_verylow=pd.DataFrame(avgsales_record_verylow).rename(columns={0: 'Product_ID', 1: 'Avg_Sales', 2: 'Promo_Bin'})

    avgsales_record_verylow = avgsales_record_verylow.merge(avgsales_record_pm14, on="Product_ID")
    avgsales_record_verylow['Avg_Sale_Diff'] = avgsales_record_verylow['Avg_Sales_x'] - avgsales_record_verylow['Avg_Sales_y']
    # avgsales_record_verylow=avgsales_record_verylow[['Product_ID','Promo_Bin_x','Avg_Sale_Diff']]
    avgsales_record_verylow['Avg_Sale_Diff_Percent'] = avgsales_record_verylow['Avg_Sale_Diff'] / avgsales_record_verylow['Avg_Sales_y']
    avgsales_record_verylow.replace([np.inf, -np.inf], np.nan, inplace=True)
    avgsales_record_verylow.dropna(subset=["Avg_Sale_Diff_Percent"], how="all", inplace=True)

    ## remove Outlier
    avgsales_record_verylow_cleaned = avgsales_record_verylow[
        (np.abs(stats.zscore(avgsales_record_verylow['Avg_Sale_Diff_Percent'])) < 3)]


    avgsales_record_verylow_sorted=avgsales_record_verylow.sort_values(by=['Avg_Sale_Diff_Percent'], ascending=False).reset_index(drop=True)
    avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent']*100
    avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent'].astype(str) + '%'

    verylow_str=str(round(avgsales_record_verylow.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0]*100,0)) + '%'
    verylow = round(avgsales_record_verylow.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)
    verylow_cleaned = round(avgsales_record_verylow_cleaned.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)
    Promotion_Effect_List.append(verylow)
    Promotion_Effect_List_cleaned.append(verylow_cleaned)

    avg_sales_with_promotion = round(avgsales_record_verylow.groupby('Promo_Bin_x')['Avg_Sales_x'].mean()[0] * 100, 0)
    avg_baseline_sales = round(avgsales_record_verylow.groupby('Promo_Bin_x')['Avg_Sales_y'].mean()[0] * 100, 0)
    Avg_Baseline_Sales_List.append(avg_baseline_sales)
    Avg_Sales_With_Promotion_List.append(avg_sales_with_promotion)

    cursor.execute(postgreSQL_select_Query_low)
    avgsales_record_low = cursor.fetchall()
    avgsales_record_low = pd.DataFrame(avgsales_record_low).rename(
        columns={0: 'Product_ID', 1: 'Avg_Sales', 2: 'Promo_Bin'})
    avgsales_record_low = avgsales_record_low.merge(avgsales_record_pm14, on="Product_ID")
    avgsales_record_low['Avg_Sale_Diff'] = avgsales_record_low['Avg_Sales_x'] - avgsales_record_low[
        'Avg_Sales_y']
    # avgsales_record_verylow=avgsales_record_verylow[['Product_ID','Promo_Bin_x','Avg_Sale_Diff']]
    avgsales_record_low['Avg_Sale_Diff_Percent'] = avgsales_record_low['Avg_Sale_Diff'] / \
                                                       avgsales_record_low['Avg_Sales_y']
    avgsales_record_low.replace([np.inf, -np.inf], np.nan, inplace=True)
    avgsales_record_low.dropna(subset=["Avg_Sale_Diff_Percent"], how="all", inplace=True)
    ## remove Outlier
    avgsales_record_low_cleaned = avgsales_record_low[
        (np.abs(stats.zscore(avgsales_record_low['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_low_sorted = avgsales_record_low.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                         ascending=False).reset_index(drop=True)
    avgsales_record_low_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_low_sorted[
                                                                  'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_low_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_low_sorted[
                                                                  'Avg_Sale_Diff_Percent'].astype(str) + '%'

    low_str = str(round(avgsales_record_low.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)) + '%'
    low = round(avgsales_record_low.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)

    low_cleaned = round(avgsales_record_low_cleaned.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,
                        0)

    Promotion_Effect_List.append(low)
    Promotion_Effect_List_cleaned.append(low_cleaned)

    avg_sales_with_promotion = round(avgsales_record_low.groupby('Promo_Bin_x')['Avg_Sales_x'].mean()[0] * 100, 0)
    avg_baseline_sales = round(avgsales_record_low.groupby('Promo_Bin_x')['Avg_Sales_y'].mean()[0] * 100, 0)
    Avg_Baseline_Sales_List.append(avg_baseline_sales)
    Avg_Sales_With_Promotion_List.append(avg_sales_with_promotion)

    cursor.execute(postgreSQL_select_Query_moderate)
    avgsales_record_moderate = cursor.fetchall()
    avgsales_record_moderate = pd.DataFrame(avgsales_record_moderate).rename(
        columns={0: 'Product_ID', 1: 'Avg_Sales', 2: 'Promo_Bin'})
    avgsales_record_moderate = avgsales_record_moderate.merge(avgsales_record_pm14, on="Product_ID")
    avgsales_record_moderate['Avg_Sale_Diff'] = avgsales_record_moderate['Avg_Sales_x'] - avgsales_record_moderate[
        'Avg_Sales_y']
    # avgsales_record_verylow=avgsales_record_verylow[['Product_ID','Promo_Bin_x','Avg_Sale_Diff']]
    avgsales_record_moderate['Avg_Sale_Diff_Percent'] = avgsales_record_moderate['Avg_Sale_Diff'] / \
                                                       avgsales_record_moderate['Avg_Sales_y']
    avgsales_record_moderate.replace([np.inf, -np.inf], np.nan, inplace=True)
    avgsales_record_moderate.dropna(subset=["Avg_Sale_Diff_Percent"], how="all", inplace=True)
    ## remove Outlier
    avgsales_record_moderate_cleaned=avgsales_record_moderate[(np.abs(stats.zscore(avgsales_record_moderate['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_moderate_sorted = avgsales_record_moderate.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                         ascending=False).reset_index(drop=True)
    avgsales_record_moderate_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_moderate_sorted[
                                                                  'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_moderate_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_moderate_sorted[
                                                                  'Avg_Sale_Diff_Percent'].astype(str) + '%'

    moderate_str = str(avgsales_record_moderate.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100) + '%'
    moderate = round(avgsales_record_moderate.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)


    moderate_cleaned = round(avgsales_record_moderate_cleaned.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,
                        0)

    Promotion_Effect_List.append(moderate)
    Promotion_Effect_List_cleaned.append(moderate_cleaned)

    avg_sales_with_promotion = round(avgsales_record_moderate.groupby('Promo_Bin_x')['Avg_Sales_x'].mean()[0] * 100, 0)
    avg_baseline_sales = round(avgsales_record_moderate.groupby('Promo_Bin_x')['Avg_Sales_y'].mean()[0] * 100, 0)
    Avg_Baseline_Sales_List.append(avg_baseline_sales)
    Avg_Sales_With_Promotion_List.append(avg_sales_with_promotion)

    cursor.execute(postgreSQL_select_Query_high)
    avgsales_record_high = cursor.fetchall()
    avgsales_record_high = pd.DataFrame(avgsales_record_high).rename(
        columns={0: 'Product_ID', 1: 'Avg_Sales', 2: 'Promo_Bin'})
    avgsales_record_high = avgsales_record_high.merge(avgsales_record_pm14, on="Product_ID")
    avgsales_record_high['Avg_Sale_Diff'] = avgsales_record_high['Avg_Sales_x'] - avgsales_record_high[
        'Avg_Sales_y']
    # avgsales_record_verylow=avgsales_record_verylow[['Product_ID','Promo_Bin_x','Avg_Sale_Diff']]
    avgsales_record_high['Avg_Sale_Diff_Percent'] = avgsales_record_high['Avg_Sale_Diff'] / \
                                                        avgsales_record_high['Avg_Sales_y']
    avgsales_record_high.replace([np.inf, -np.inf], np.nan, inplace=True)

    avgsales_record_high.dropna(subset=["Avg_Sale_Diff_Percent"], how="all", inplace=True)

    ## Remove Outlier
    avgsales_record_high_cleaned = avgsales_record_high[
        (np.abs(stats.zscore(avgsales_record_high['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_high_sorted = avgsales_record_high.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                           ascending=False).reset_index(drop=True)
    avgsales_record_high_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_high_sorted[
                                                                   'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_high_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_high_sorted[
                                                                   'Avg_Sale_Diff_Percent'].astype(str) + '%'
    avgsales_record_high_sorted

    high = round(avgsales_record_high.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100, 0)


    high_cleaned = round(avgsales_record_high_cleaned.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,
                             0)

    Promotion_Effect_List.append(high)
    Promotion_Effect_List_cleaned.append(high_cleaned)

    avg_sales_with_promotion = round(avgsales_record_high.groupby('Promo_Bin_x')['Avg_Sales_x'].mean()[0] * 100, 0)
    avg_baseline_sales = round(avgsales_record_high.groupby('Promo_Bin_x')['Avg_Sales_y'].mean()[0] * 100, 0)
    Avg_Baseline_Sales_List.append(avg_baseline_sales)
    Avg_Sales_With_Promotion_List.append(avg_sales_with_promotion)



    cursor.execute(postgreSQL_select_Query_veryhigh)
    avgsales_record_veryhigh = cursor.fetchall()
    avgsales_record_veryhigh = pd.DataFrame(avgsales_record_veryhigh).rename(
        columns={0: 'Product_ID', 1: 'Avg_Sales', 2: 'Promo_Bin'})
    avgsales_record_veryhigh = avgsales_record_veryhigh.merge(avgsales_record_pm14, on="Product_ID")
    avgsales_record_veryhigh['Avg_Sale_Diff'] = avgsales_record_veryhigh['Avg_Sales_x'] - avgsales_record_veryhigh[
        'Avg_Sales_y']
    # avgsales_record_verylow=avgsales_record_verylow[['Product_ID','Promo_Bin_x','Avg_Sale_Diff']]
    avgsales_record_veryhigh['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh['Avg_Sale_Diff'] / avgsales_record_veryhigh['Avg_Sales_y']
    avgsales_record_veryhigh.replace([np.inf, -np.inf], np.nan, inplace=True)
    avgsales_record_veryhigh.dropna(subset=["Avg_Sale_Diff_Percent"], how="all", inplace=True)

    ## Remove Outlier
    avgsales_record_veryhigh_cleaned=avgsales_record_veryhigh[(np.abs(stats.zscore(avgsales_record_veryhigh['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_veryhigh_sorted = avgsales_record_veryhigh.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                   ascending=False).reset_index(drop=True)
    avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh_sorted[
                                                               'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'].apply(lambda x: round(x, 0))

    avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh_sorted[
                                                                   'Avg_Sale_Diff_Percent'].astype(str) + '%'

    very_high_str = str(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100) + '%'
    very_high = round(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100, 0)


    very_high_cleaned = round(avgsales_record_veryhigh_cleaned.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,
                         0)

    Promotion_Effect_List.append(very_high)
    Promotion_Effect_List_cleaned.append(very_high_cleaned)

    avg_sales_with_promotion = round(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sales_x'].mean()[0] * 100, 0)
    avg_baseline_sales = round(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sales_y'].mean()[0] * 100, 0)
    Avg_Baseline_Sales_List.append(avg_baseline_sales)
    Avg_Sales_With_Promotion_List.append(avg_sales_with_promotion)

    Promotion_Effect_List



## General Effect Of Promotion ( Does not measure the specific sales increase over different products)
    fig_avg_total = plt.figure()
    df_Promotion_bin = pd.DataFrame({
        'Promotion_Tier': Promotion_Bin_Tier_List,
        'Baseline AvgSales': Avg_Baseline_Sales_List,
        'AvgSales Under Promotion': Avg_Sales_With_Promotion_List
    })
    fig_avg_total, ax1 = plt.subplots(figsize=(10, 10))
    tidy = df_Promotion_bin.melt(id_vars='Promotion_Tier').rename(columns=str.title)
    seaborn.barplot(x='Promotion_Tier', y='Value', hue='Variable', data=tidy, ax=ax1)
    seaborn.despine(fig_avg_total)


## AvgSales increase of every specific products with Promotion
    fig_diff = plt.figure()
    df_Promotion_bin = pd.DataFrame({
        'Promotion_Tier': Promotion_Bin_Tier_List,
        'Promotion_Effect(%)': Promotion_Effect_List
    })

    ax = seaborn.barplot(x='Promotion_Tier', y='Promotion_Effect(%)',
                     data=df_Promotion_bin,
                     errwidth=0)
    ax.bar_label(ax.containers[0])

## AvgPercentSales increase of every specific products with Promotion without outliers
    fig_cleaned = plt.figure()
    df_Promotion_bin = pd.DataFrame({
        'Promotion_Tier': Promotion_Bin_Tier_List,
        'Promotion_Effect(%)': Promotion_Effect_List_cleaned
    })

    ax = seaborn.barplot(x='Promotion_Tier', y='Promotion_Effect(%)',
                     data=df_Promotion_bin,
                     errwidth=0)
    ax.bar_label(ax.containers[0])
    return fig_avg_total,fig_diff,fig_cleaned



