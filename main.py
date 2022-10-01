# Imports
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


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass

# start command line tool
parser = argparse.ArgumentParser(prog='superpy', description='Inventory system')
subparser = parser.add_subparsers(dest='command')

# command line to show inventory
inventory = subparser.add_parser('in_stock')

# command line to show sold products.
sold_products = subparser.add_parser('sold_products')
sold_products.add_argument(
    'date', type=str, choices=['today', 'yesterday', 'last_month', 'all'],
    help='choose between: today, yesterday, last_month or all')

# command line to show bought products.
bought_products = subparser.add_parser('bought_products')
bought_products.add_argument(
    'date', type=str, choices=['today', 'yesterday', 'last_month', 'all'],
    help='choose between: today, yesterday, last_month or all')

# command line to update expired products
expired = subparser.add_parser('expired')
expired.add_argument('show', type=str, 
    choices=['today', 'yesterday', 'last_month', 'all', 'update'], 
    help='choose between: today, yesterday, last_month, all or update')

# command line to add a bought product.
buy = subparser.add_parser('buy')
buy.add_argument('-product_name', type=str, help='name of the product')
buy.add_argument('-buy_price', type=float, help="price paid for 1 product in 0.00 euro's")
buy.add_argument('-quantity', type=int, help= 'amount of bought products')
buy.add_argument('-expiration_date', type=str, help='date in yyyy-mm-dd when product expired')

# command line to sell a product.
sell = subparser.add_parser('sell')
sell.add_argument('-product_name', type=str, help= 'name of the product')
sell.add_argument('-sell_price', type=float, help= "price for 1 sold product in 0.00 euro's")
sell.add_argument('-quantity', type=int, help= 'amount of sold products')

# command line to make pdf for charity
charity = subparser.add_parser('charity')

# command line for revenue and profit
revenue = subparser.add_parser('revenue')
revenue.add_argument('show', type=str, choices=['today', 'yesterday', 'last_month', 'last_year'], 
                        help='choose between: today, yesterday, last_month or last_year')

profit = subparser.add_parser('profit')
profit.add_argument('show', type=str, choices=['today', 'yesterday', 'last_month', 'last_year'], 
                        help='choose between: today, yesterday, last_month or last_year')

# command line for advanced time
advance_time = subparser.add_parser('advance_time')
advance_time.add_argument('number', type=int, 
                        help='the amount of days you will look in advance')

args = parser.parse_args()


# open en show csv files
def instock():
    df = pd.read_csv('superpy/instock.csv')
    table = Table(show_header=True, header_style="bold dark_blue", style="on white", show_lines=True)
    table.row_styles = ["black", "dark_magenta"]
    return df_to_table(df, table, False)


def show_sold():
    df = pd.read_csv('superpy/sold.csv')
    table = Table(show_header=True, header_style="bold bright_yellow", style="on black", show_lines=True)
    table.row_styles = ["grey50", "dim"]

    if args.date == 'today':
        return df_to_table((df[(df['sell_date'] == date_today)]), table, False)
    elif args.date == 'yesterday':
        return df_to_table((df[(df['sell_date'] == date_yesterday)]), table, False)
    elif args.date == 'last_month':
        return df_to_table((df[(df['sell_date'] >= date_last_month)]), table, False)
    elif args.date == 'all':
        return df_to_table(df, table, False)
    else:
        print('Invalid usage')


def show_bought():
    df = pd.read_csv('superpy/bought.csv')
    table = Table(show_header=True, header_style="bold magenta", style="on navy_blue", show_lines=True)
    table.row_styles = ["grey50", "dim"]
    
    if args.date == 'today':
        return df_to_table((df[(df['buy_date'] == date_today)]), table, False)
    elif args.date == 'yesterday':
        return df_to_table((df[(df['buy_date'] == date_yesterday)]), table, False)
    elif args.date == 'last_month':
        return df_to_table((df[(df['buy_date'] >= date_last_month)]), table, False)
    elif args.date == 'all':
        return df_to_table(df, table, False)
        
    else:
        print('Invalid usage')


def show_expired():
    # update expired products
    df = pd.read_csv('superpy/instock.csv')
    df_ex = pd.read_csv('superpy/expired.csv')
    table = Table(show_header=True, header_style="bold dark_green", style="on grey66", show_lines=True)
    table.row_styles = ["dark_red", "bright_red"]
    if args.show == 'update':
        if date_today == date.today().strftime("%Y-%m-%d"):
            expired_product = df.loc[df["expiration_date"] < date_today]
            pd.concat([df_ex, expired_product]).to_csv('superpy/expired.csv', index= False)
            df.loc[df["expiration_date"] >= date_today].to_csv('superpy/instock.csv', index= False)
            return 'OK'
        else:
            print('set advance_time to 0 first')
    # show expired products
    elif args.show == 'today':
        return df_to_table((df[(df['expiration_date'] == date_today)]), table, False)
    elif args.show == 'yesterday':
        return df_to_table((df_ex[(df_ex['expiration_date'] == date_yesterday)]), table, False)
    elif args.show == 'last_month':
        return df_to_table((df_ex[(df_ex['expiration_date'] >= date_last_month)]), table, False)
    elif args.show == 'all':
        return df_to_table(df_ex, table, False)
    else:
        print('Invalid usage')
   

# write csv files
def buy_product():
    # check if expiration_date is in the correct format.
    try:
        datetime.strptime(args.expiration_date, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format, should be YYYY-MM-DD")
    with open('superpy/bought.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        # making an ID
        rowcount  = 0
        for row in open("superpy/bought.csv"):
            rowcount+= 1
        # Add contents of list as last row in the csv file
        csv_writer.writerow([rowcount, args.product_name, args.buy_price, 
            args.quantity, args.expiration_date, date.today().strftime("%Y-%m-%d")])
        # Add new products to instock file
        with open('superpy/instock.csv', 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow([args.product_name, rowcount, args.quantity, args.expiration_date])
            return 'OK'
            

def sell_product():
    with open('superpy/sold.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        # making an ID
        rowcount  = 0
        for row in open("superpy/sold.csv"):
            rowcount+= 1
        # match bought_id
        df = pd.read_csv('superpy/instock.csv', index_col='product_name')
        bought_id = df.loc[args.product_name, 'bought_id']
        if change_quantity() == 'OK':
            # Add contents as last row in the csv file    
            csv_writer.writerow([rowcount, bought_id, args.product_name, 
                args.sell_price, args.quantity, date.today().strftime("%Y-%m-%d")])
            return 'OK'


def change_quantity():
    # look if product is in stock.
    df = pd.read_csv('superpy/instock.csv', index_col='product_name')
        # look if enough products are in stock
    try:
        if (df.loc[args.product_name, 'quantity'] -args.quantity) < 0:
            print('not enough product in stock')
        df.loc[args.product_name, 'quantity'] = (df.loc[args.product_name, 'quantity'] -args.quantity)
        # Write new quantity to CSV file
        df.to_csv('superpy/instock.csv') 
    except KeyError:
        print ('This product is not in stock')
    return 'OK'


def show_charity():
    df = pd.read_csv('superpy/instock.csv')
    df1 = df.loc[df['expiration_date'] == date_tomorrow].drop('bought_id', axis=1)
    fig, ax =plt.subplots(figsize=(10,4))
    ax.axis('tight')
    ax.axis('off')
    try:
        the_table = ax.table(cellText=df1.values,colLabels=df1.columns,cellLoc='right')
        pp = PdfPages("superpy/charity_pdf_files/charity.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()
        return 'PDF file made'
    except IndexError:
        print('No products for charity today')


def show_revenue():
    df = pd.read_csv('superpy/sold.csv')
    if args.show == 'today':
        df1 = df.loc[df['sell_date'] == date_today]
        revenue_today = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue today: {revenue_today}'
    elif args.show == 'yesterday':
        df1 = df.loc[df['sell_date'] == date_yesterday]
        revenue_yesterday = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue yesterday: {revenue_yesterday}'
    elif args.show == 'last_month':
        df1 = df.loc[df['sell_date'] == date_last_month]
        revenue_last_month = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue last month: {revenue_last_month}'
    elif args.show == 'last_year':
        df1 = df.loc[df['sell_date'] == date_last_year]
        revenue_last_year = (df1['quantity'] * df1['sell_price']).sum()
        return f'revenue last year: {revenue_last_year}'
    else:
        print('Invalid usage')


def show_profit():
    df_s = pd.read_csv('superpy/sold.csv')
    df_b = pd.read_csv('superpy/bought.csv')
    df1 = df_s.merge(df_b.rename(columns={'id': 'bought_id'}),on= 'bought_id')
    if args.show == 'today':
        df2 = df1.loc[df1['sell_date'] == date_today]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_today = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit today: {revenue_today - cost}'
    elif args.show == 'yesterday':
        df2 = df1.loc[df1['sell_date'] == date_yesterday]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_yesterday = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit yesterday: {revenue_yesterday - cost}'
    elif args.show == 'last_month':
        df2 = df1.loc[df1['sell_date'] == date_last_month]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_last_month = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit last month: {revenue_last_month - cost}'
    elif args.show == 'last_year':
        df2 = df1.loc[df1['sell_date'] == date_last_year]
        cost = (df2['buy_price'] * df2['quantity_x']).sum()
        revenue_last_year = (df2['quantity_x'] * df2['sell_price']).sum()
        return f'profit last year: {revenue_last_year - cost}'
    else:
        print('Invalid usage')


def advancetime():
    with open('superpy/date.txt', 'w') as date_file:
        new_date = date.today() + timedelta(days= args.number)
        date_file.write(str(new_date))
        print('OK')


def datetoday():
    with open('superpy/date.txt', 'r') as file:
        date = file.read()
        return date

date_today = datetoday()  # date.today().strftime("%Y-%m-%d")
date_yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
date_last_month = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
date_last_year = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
date_tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

console = Console()

if __name__ == "__main__":
    if args.command == 'in_stock':
        print(instock())
    elif args.command == 'buy':
        print(buy_product())
    elif args.command == 'sell':
        print(sell_product())
    elif args.command == 'sold_products':
        print(show_sold())
    elif args.command == 'bought_products':
        print(show_bought())
    elif args.command == 'expired':
        print(show_expired())
    elif args.command == 'revenue':
        print(show_revenue())
    elif args.command == 'profit':
        print(show_profit())
    elif args.command == 'advance_time':
        print(advancetime())
    elif args.command == 'charity':
        print(show_charity())
    main()
