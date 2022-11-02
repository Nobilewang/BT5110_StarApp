from flask import Flask,jsonify,url_for,redirect,request,render_template
from flask_sqlalchemy import SQLAlchemy
import config
from apps.book import bp as book_bp
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
# from flask_migrate import Migrate
import matplotlib.pyplot as plt
import seaborn
import psycopg2

import pandas as pd

from sqlalchemy import create_engine


# df_sale=pd.read_csv("C:\\Users\\Yijie\\Documents\\WeChat Files\\wxid_alrm02jw70ea22\\FileStorage\\File\\2022-10\\sales.csv")
# df_product=pd.read_csv("C:\\Users\\Yijie\\Documents\\WeChat Files\\wxid_alrm02jw70ea22\\FileStorage\\File\\2022-10\\product_hierarchy_final_processed.csv")
# df_store=pd.read_csv("C:\\Users\\Yijie\\Documents\\WeChat Files\\wxid_alrm02jw70ea22\\FileStorage\\File\\2022-10\\store_cities_final_processed.csv")
# df_date=pd.read_csv("C:\\Users\\Yijie\\Documents\\WeChat Files\\wxid_alrm02jw70ea22\\FileStorage\\File\\2022-10\\date(2).csv")
# df_promotion=df_sale[['product_id','store_id','date','promo_type_1','promo_bin_1']]
USERNAME='Gaoda'
PASSWORD='Gaoda'
DATABASE='StarAPP'
DB_URI='postgresql+psycopg2://{}:{}@localhost:5432/{}'.format(USERNAME,PASSWORD,DATABASE)
engine = create_engine(DB_URI)
# df_sale.to_sql('Sales', engine)
# df_promotion.to_sql('Promotion', engine)
# with engine.connect() as con:
#     con.execute('select')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def plot_function(p1='na', p2='na', p3='na', check_single_date='no'):
    if p1 == 'na' and p2 == 'na' and p3 == 'na' and check_single_date == 'no':
        print('Null value of the date blank is not acceptable!!!')
    else:
        connection = psycopg2.connect(user="Gaoda",
                                      password="Gaoda",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="StarAPP")
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
            postgreSQL_select_Query = "select AVG(s.revenue) from

    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    plot_df = pd.DataFrame(mobile_records, columns=['Average Revenue', 'month'])

    if p1 == 'date':
        fig = plt.figure()
        plt.plot(plot_df['month'], plot_df['Average Revenue'])
        plt.show()

    else:
        fig = plt.figure()
        plt.plot(plot_df['month'], plot_df['Average Revenue'], 'g*-')
        for a, b in zip(plot_df['month'], np.round(np.array(plot_df['Average Revenue']), 2)):
            plt.text(a, b + 0.001, '%.2f' % b, ha='center', va='bottom', fontsize=9)
        plt.show()

plot_function(p1='month', p2='S0002')


postgreSQL_select_Query = "select p.hierarchy1_id, p.hierarchy2_id, sum(s.revenue), sum(s.sales) from products p, sales s where p.hierarchy1_id='H00' and p.product_id = s.product_id Group by p.hierarchy1_id , p.hierarchy2_id".format(
                p1, p1, p1)

def QRcode(h=0):
    connection = psycopg2.connect(user="Gaoda",
                                  password="Gaoda",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="StarAPP")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from public.sales s, public.products p where p.product_id = s.product_id"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    mobile_records = pd.DataFrame(mobile_records)

    if h == 1:
        mobile_records=mobile_records.groupby(12)[[3,4]].sum().rename(columns = {3:'Total_Sales',4:'Total_Revenue'}).rename_axis('hierarchy1')
    if h == 2:
        mobile_records = mobile_records.groupby(13)[[3, 4]].sum().rename(
            columns={3: 'Total_Sales', 4: 'Total_Revenue'}).rename_axis('hierarchy2')
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')


    table = ax.table(cellText=mobile_records.values, colLabels=mobile_records.columns,rowLabels=mobile_records.index, loc='center')
    table.add_cell(0, -1, w, h, text=mobile_records.index.name)
    fig.tight_layout()

    plt.show()
QRcode(h=1)

def Store_analysis():
    connection = psycopg2.connect(user="Gaoda",
                                  password="Gaoda",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="StarAPP")
    cursor = connection.cursor()
    postgreSQL_select_Query = 'select st.store_id, st.store_size, st.city_id , sum(s.revenue) as "Total Revenue", sum(s.sales) as "Total Sales" from sales s, stores st where st.store_id = s.store_id Group by  st.store_id, st.store_size, st.city_id order by st.store_size ASC'
    cursor.execute(postgreSQL_select_Query)
    store_records = cursor.fetchall()
    store_records = pd.DataFrame(store_records).rename(columns={0: 'Store_ID', 1: 'Store_Size', 2: 'City_ID', 3: 'Total_Revenue', 4: 'Total_Sales'})
    fig, ax = plt.subplots()

    # hide axesconnection = psycopg2.connect(user="Gaoda",
    #                                   password="Gaoda",
    #                                   host="127.0.0.1",
    #                                   port="5432",
    #                                   database="StarAPP")
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    table = ax.table(cellText=store_records.values, colLabels=store_records.columns,
                     loc='center')
    # table.add_cell(0, -1, w, h, text=store_records.index.name)
    fig.tight_layout()

    plt.show()

#Cannibalization Analysis
    connection = psycopg2.connect(user="Gaoda",
                                  password="Gaoda",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="StarAPP")
    cursor = connection.cursor()
    Promotion_Effect_List=[]
    Avg_Sales_With_Promotion_List=[]
    Avg_Baseline_Sales_List=[]
    Promotion_Bin_Tier_List=['VERY_LOW','LOW','MODERATE','HIGH','VERYHIGH']
    # PM14
    postgreSQL_select_Query_PM14 = "select s.product_id, avg (s.sales), p.promo_bin from sales s , promotion p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type and p.promo_bin = 'NO_RECORD' GROUP by s.product_id,  p.promo_bin"
    #verylow
    postgreSQL_select_Query_verylow = "select s.product_id, avg (s.sales), p.promo_bin from sales s , promotion p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type and p.promo_bin = 'verylow' GROUP by s.product_id,  p.promo_bin"
    # low
    postgreSQL_select_Query_low = "select s.product_id, avg (s.sales), p.promo_bin from sales s , promotion p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type and p.promo_bin = 'low' GROUP by s.product_id,  p.promo_bin"
    # moderate
    postgreSQL_select_Query_moderate = "select s.product_id, avg (s.sales), p.promo_bin from sales s , promotion p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type and p.promo_bin = 'moderate' GROUP by s.product_id,  p.promo_bin"
    # high
    postgreSQL_select_Query_high = "select s.product_id, avg (s.sales), p.promo_bin from sales s , promotion p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type and p.promo_bin = 'high' GROUP by s.product_id,  p.promo_bin"
    # veryhigh
    postgreSQL_select_Query_veryhigh = "select s.product_id, avg (s.sales), p.promo_bin from sales s , promotion p where s.product_id= p.product_id and s.date = p.date and s.store_id = p.store_id and s.promo_type_1= p.promo_type and p.promo_bin = 'veryhigh' GROUP by s.product_id,  p.promo_bin"

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
    avgsales_record_verylow = avgsales_record_verylow[
        (np.abs(stats.zscore(avgsales_record_verylow['Avg_Sale_Diff_Percent'])) < 3)]


    avgsales_record_verylow_sorted=avgsales_record_verylow.sort_values(by=['Avg_Sale_Diff_Percent'], ascending=False).reset_index(drop=True)
    avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent']*100
    avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_verylow_sorted['Avg_Sale_Diff_Percent'].astype(str) + '%'
    avgsales_record_verylow_sorted

    verylow_str=str(round(avgsales_record_verylow.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0]*100,0)) + '%'
    verylow = round(avgsales_record_verylow.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)
    verylow_str
    verylow
    Promotion_Effect_List.append(verylow)

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
    avgsales_record_low = avgsales_record_low[
        (np.abs(stats.zscore(avgsales_record_low['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_low_sorted = avgsales_record_low.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                         ascending=False).reset_index(drop=True)
    avgsales_record_low_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_low_sorted[
                                                                  'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_low_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_low_sorted[
                                                                  'Avg_Sale_Diff_Percent'].astype(str) + '%'
    avgsales_record_low_sorted

    low_str = str(round(avgsales_record_low.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)) + '%'
    low = round(avgsales_record_low.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)
    low_str
    low
    Promotion_Effect_List.append(low)

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
    avgsales_record_moderate=avgsales_record_moderate[(np.abs(stats.zscore(avgsales_record_moderate['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_moderate_sorted = avgsales_record_moderate.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                         ascending=False).reset_index(drop=True)
    avgsales_record_moderate_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_moderate_sorted[
                                                                  'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_moderate_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_moderate_sorted[
                                                                  'Avg_Sale_Diff_Percent'].astype(str) + '%'
    avgsales_record_moderate_sorted

    moderate_str = str(avgsales_record_moderate.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100) + '%'
    moderate = round(avgsales_record_moderate.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100,0)
    moderate_str
    moderate
    Promotion_Effect_List.append(moderate)

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
    avgsales_record_high = avgsales_record_high[
        (np.abs(stats.zscore(avgsales_record_high['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_high_sorted = avgsales_record_high.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                           ascending=False).reset_index(drop=True)
    avgsales_record_high_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_high_sorted[
                                                                   'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_high_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_high_sorted[
                                                                   'Avg_Sale_Diff_Percent'].astype(str) + '%'
    avgsales_record_high_sorted

    high = round(avgsales_record_high.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100, 0)
    high
    Promotion_Effect_List.append(high)
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
    avgsales_record_veryhigh=avgsales_record_veryhigh[(np.abs(stats.zscore(avgsales_record_veryhigh['Avg_Sale_Diff_Percent'])) < 3)]

    avgsales_record_veryhigh_sorted = avgsales_record_veryhigh.sort_values(by=['Avg_Sale_Diff_Percent'],
                                                                   ascending=False).reset_index(drop=True)
    avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh_sorted[
                                                               'Avg_Sale_Diff_Percent'] * 100
    avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'].apply(lambda x: round(x, 0))

    avgsales_record_veryhigh_sorted['Avg_Sale_Diff_Percent'] = avgsales_record_veryhigh_sorted[
                                                                   'Avg_Sale_Diff_Percent'].astype(str) + '%'

    very_high_str = str(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100) + '%'
    very_high = round(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sale_Diff_Percent'].mean()[0] * 100, 0)
    very_high_str
    very_high
    Promotion_Effect_List.append(very_high)

    avg_sales_with_promotion = round(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sales_x'].mean()[0] * 100, 0)
    avg_baseline_sales = round(avgsales_record_veryhigh.groupby('Promo_Bin_x')['Avg_Sales_y'].mean()[0] * 100, 0)
    Avg_Baseline_Sales_List.append(avg_baseline_sales)
    Avg_Sales_With_Promotion_List.append(avg_sales_with_promotion)

    Promotion_Effect_List



## General Effect Of Promotion ( Does not measure the specific sales increase over different products)
    df_Promotion_bin = pd.DataFrame({
        'Promotion_Tier': Promotion_Bin_Tier_List,
        'Baseline AvgSales': Avg_Baseline_Sales_List,
        'AvgSales Under Promotion': Avg_Sales_With_Promotion_List
    })
    fig, ax1 = plt.subplots(figsize=(10, 10))
    tidy = df_Promotion_bin.melt(id_vars='Promotion_Tier').rename(columns=str.title)
    seaborn.barplot(x='Promotion_Tier', y='Value', hue='Variable', data=tidy, ax=ax1)
    seaborn.despine(fig)
    plt.show()


## AvgSales increase of every specific products with Promotion

    df_Promotion_bin = pd.DataFrame({
        'Promotion_Tier': Promotion_Bin_Tier_List,
        'Promotion_Effect(%)': Promotion_Effect_List
    })

    ax = seaborn.barplot(x='Promotion_Tier', y='Promotion_Effect(%)',
                     data=df_Promotion_bin,
                     errwidth=0)
    ax.bar_label(ax.containers[0])
    plt.show()



##

    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    table = ax.table(cellText=store_records.values, colLabels=store_records.columns,
                     loc='center')
    # table.add_cell(0, -1, w, h, text=store_records.index.name)
    fig.tight_layout()

    plt.show()