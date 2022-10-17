import argparse
import csv
from datetime import datetime, date, timedelta
import pandas as pd
from rich_tools import df_to_table
from rich import print
from rich.table import Table
from rich.console import Console
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import main as m

# open en show csv files
def instock():
    df = pd.read_csv('instock.csv')
    table = Table(show_header=True, header_style="bold dark_blue", style="on white", show_lines=True)
    table.row_styles = ["black", "dark_magenta"]
    return df_to_table(df, table, False)


def show_sold():
    df = pd.read_csv('sold.csv')
    table = Table(show_header=True, header_style="bold bright_yellow", style="on black", show_lines=True)
    table.row_styles = ["grey50", "dim"]

    if m.args.date == 'today':
        return df_to_table((df[(df['sell_date'] == date_today)]), table, False)
    elif m.args.date == 'yesterday':
        return df_to_table((df[(df['sell_date'] == date_yesterday)]), table, False)
    elif m.args.date == 'last_month':
        return df_to_table((df[(df['sell_date'] >= date_last_month)]), table, False)
    elif m.args.date == 'all':
        return df_to_table(df, table, False)
    else:
        print('Invalid usage')


def show_bought():
    df = pd.read_csv('bought.csv')
    table = Table(show_header=True, header_style="bold magenta", style="on navy_blue", show_lines=True)
    table.row_styles = ["grey50", "dim"]
    
    if m.args.date == 'today':
        return df_to_table((df[(df['buy_date'] == date_today)]), table, False)
    elif m.args.date == 'yesterday':
        return df_to_table((df[(df['buy_date'] == date_yesterday)]), table, False)
    elif m.args.date == 'last_month':
        return df_to_table((df[(df['buy_date'] >= date_last_month)]), table, False)
    elif m.args.date == 'all':
        return df_to_table(df, table, False)
        
    else:
        print('Invalid usage')


def show_expired():
    # update expired products
    df = pd.read_csv('instock.csv')
    df_ex = pd.read_csv('expired.csv')
    table = Table(show_header=True, header_style="bold dark_green", style="on grey66", show_lines=True)
    table.row_styles = ["dark_red", "bright_red"]
    if m.args.show == 'update':
        if date_today == date.today().strftime("%Y-%m-%d"):
            expired_product = df.loc[df["expiration_date"] < date_today]
            pd.concat([df_ex, expired_product]).to_csv('expired.csv', index= False)
            df.loc[df["expiration_date"] >= date_today].to_csv('instock.csv', index= False)
            return 'OK'
        else:
            return 'set advance_time to 0 first'
    # show expired products
    elif m.args.show == 'today':
        return df_to_table((df[(df['expiration_date'] == date_today)]), table, False)
    elif m.args.show == 'yesterday':
        return df_to_table((df_ex[(df_ex['expiration_date'] == date_yesterday)]), table, False)
    elif m.args.show == 'last_month':
        return df_to_table((df_ex[(df_ex['expiration_date'] >= date_last_month)]), table, False)
    elif m.args.show == 'all':
        return df_to_table(df_ex, table, False)
    else:
        print('Invalid usage')
   

# write csv files
def buy_product():
    # check if expiration_date is in the correct format.
    try:
        datetime.strptime(m.args.expiration_date, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format, should be YYYY-MM-DD")
    with open('bought.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        # making an ID
        rowcount  = 0
        for row in open("bought.csv"):
            rowcount+= 1
        # Add contents of list as last row in the csv file
        csv_writer.writerow([rowcount, m.args.product_name, m.args.buy_price, 
            m.args.quantity, m.args.expiration_date, date.today().strftime("%Y-%m-%d")])
        # Add new products to instock file
        with open('instock.csv', 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow([m.args.product_name, rowcount, m.args.quantity, m.args.expiration_date])
            return 'OK'
            

def sell_product():
    with open('sold.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        # making an ID
        rowcount  = 0
        for row in open("sold.csv"):
            rowcount+= 1
        # match bought_id
        df = pd.read_csv('instock.csv', index_col='product_name')
        try:
            df2 = df.loc[m.args.product_name].sort_values('expiration_date')
            bought_id = df2.iloc[0,0]
        except ValueError:
            bought_id = df.loc[m.args.product_name, 'bought_id']
        if change_quantity() == 'OK':
            # Add contents as last row in the csv file    
            csv_writer.writerow([rowcount, bought_id, m.args.product_name, 
                m.args.sell_price, m.args.quantity, date.today().strftime("%Y-%m-%d")])
            return 'OK'



def change_quantity():
    # look if product is in stock.
    df = pd.read_csv('instock.csv', index_col= 'product_name')
    df1 = pd.read_csv('instock.csv')
    df6 = df1.set_index('bought_id')
    if df1['product_name'].str.contains(m.args.product_name).sum() > 1:
        df2 = (df.loc[m.args.product_name]).sort_values('expiration_date')
        id_old = df2.iloc[0,0]
        if (df6.loc[id_old, 'quantity'] -m.args.quantity) == 0:
            df6 = df6.drop(id_old).reset_index().set_index('product_name')
            df6.to_csv('instock.csv')
            return 'OK'
        elif (df6.loc[id_old, 'quantity'] -m.args.quantity) < 0:
            print('Not enough product in stock')
        else:
            df6.loc[id_old, 'quantity'] = (df6.loc[id_old, 'quantity']- m.args.quantity)
            df6 = df6.reset_index().set_index('product_name')
            df6.to_csv('instock.csv')
            return 'OK'   
    # look if enough products are in stock
    elif (df.loc[m.args.product_name, 'quantity'] -m.args.quantity) >= 0:
        df.loc[m.args.product_name, 'quantity'] = (df.loc[m.args.product_name, 'quantity'] -m.args.quantity)
        # Write new quantity to CSV file
        df.to_csv('instock.csv')
        return 'OK'

    




def show_charity():
    df = pd.read_csv('instock.csv')
    df1 = df.loc[df['expiration_date'] == date_tomorrow].drop('bought_id', axis=1)
    fig, ax =plt.subplots(figsize=(10,4))
    ax.axis('tight')
    ax.axis('off')
    try:
        the_table = ax.table(cellText=df1.values,colLabels=df1.columns,cellLoc='right')
        pp = PdfPages("charity_pdf_files/charity.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()
        return 'PDF file made'
    except IndexError:
        print('No products for charity today')


def show_revenue():
    df = pd.read_csv('sold.csv')
    if m.args.show == 'today':
        df1 = df.loc[df['sell_date'] == date_today]
        revenue_today = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue today: {revenue_today}'
    elif m.args.show == 'yesterday':
        df1 = df.loc[df['sell_date'] == date_yesterday]
        revenue_yesterday = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue yesterday: {revenue_yesterday}'
    elif m.args.show == 'last_month':
        df1 = df.loc[df['sell_date'] >= date_last_month]
        revenue_last_month = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue last month: {revenue_last_month}'
    elif m.args.show == 'last_year':
        df1 = df.loc[df['sell_date'] >= date_last_year]
        revenue_last_year = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue last year: {revenue_last_year}'
    else:
        print('Invalid usage')


def show_profit():
    df_s = pd.read_csv('sold.csv')
    df_b = pd.read_csv('bought.csv')
    df1 = df_s.merge(df_b.rename(columns={'id': 'bought_id'}),on= 'bought_id')
    if m.args.show == 'today':
        df2 = df1.loc[df1['sell_date'] == date_today]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_today = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit today: {revenue_today - cost}'
    elif m.args.show == 'yesterday':
        df2 = df1.loc[df1['sell_date'] == date_yesterday]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_yesterday = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit yesterday: {revenue_yesterday - cost}'
    elif m.args.show == 'last_month':
        df2 = df1.loc[df1['sell_date'] >= date_last_month]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_last_month = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit last month: {revenue_last_month - cost}'
    elif m.args.show == 'last_year':
        df2 = df1.loc[df1['sell_date'] >= date_last_year]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_last_year = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit last year: {revenue_last_year - cost}'
    else:
        print('Invalid usage')


def advancetime():
    with open('date.txt', 'w') as date_file:
        new_date = date.today() + timedelta(days= m.args.number)
        date_file.write(str(new_date))
        return 'OK'


def datetoday():
    with open('date.txt', 'r') as file:
        date = file.read()
        return date

date_today = datetoday()  # date.today().strftime("%Y-%m-%d")
date_yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
date_last_month = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
date_last_year = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
date_tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")