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
import mainfunctions as fc


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
inventory = subparser.add_parser('in_stock', help= 'Shows a report of the inventory.')

# command line to show sold products.
sold_products = subparser.add_parser('sold_products', help= 'Shows a report of the sold products.')
sold_products.add_argument(
    'date', type=str, choices=['today', 'yesterday', 'last_month', 'all'],
    help='choose between: today, yesterday, last_month or all')

# command line to show bought products.
bought_products = subparser.add_parser('bought_products', help= 'Shows a report of the bought products.')
bought_products.add_argument(
    'date', type=str, choices=['today', 'yesterday', 'last_month', 'all'],
    help='choose between: today, yesterday, last_month or all')

# command line to update expired products
expired = subparser.add_parser('expired', help= 'Update and shows a report of the expired products')
expired.add_argument('show', type=str, 
    choices=['today', 'yesterday', 'last_month', 'all', 'update'], 
    help='choose between: today, yesterday, last_month, all or update')

# command line to add a bought product.
buy = subparser.add_parser('buy', help= 'Use this to buy a product.')
buy.add_argument('-product_name', type=str, help='name of the product')
buy.add_argument('-buy_price', type=float, help="price paid for 1 product in 0.00 euro's")
buy.add_argument('-quantity', type=int, help= 'amount of bought products')
buy.add_argument('-expiration_date', type=str, help='date in yyyy-mm-dd when product expired')

# command line to sell a product.
sell = subparser.add_parser('sell', help= 'Use this to sell a product.')
sell.add_argument('-product_name', type=str, help= 'name of the product')
sell.add_argument('-sell_price', type=float, help= "price for 1 sold product in 0.00 euro's")
sell.add_argument('-quantity', type=int, help= 'amount of sold products')

# command line to make pdf for charity
charity = subparser.add_parser('charity', help= 'Make a pdf file with products wich are good for charity.')

# command line for revenue and profit
revenue = subparser.add_parser('revenue', help= 'Shows the revenue of a certain period.')
revenue.add_argument('show', type=str, choices=['today', 'yesterday', 'last_month', 'last_year'], 
                        help='choose between: today, yesterday, last_month or last_year')

profit = subparser.add_parser('profit', help= 'Shows the profit of a certain period.')
profit.add_argument('show', type=str, choices=['today', 'yesterday', 'last_month', 'last_year'], 
                        help='choose between: today, yesterday, last_month or last_year')

# command line for advanced time
advance_time = subparser.add_parser('advance_time', help= 'Change the date of the system per day.')
advance_time.add_argument('number', type=int, 
                        help='the amount of days you will look in advance')

args = parser.parse_args()


console = Console()

if __name__ == "__main__":
    if args.command == 'in_stock':
        print(fc.instock())
    elif args.command == 'buy':
        print(fc.buy_product())
    elif args.command == 'sell':
        print(fc.sell_product())
    elif args.command == 'sold_products':
        print(fc.show_sold())
    elif args.command == 'bought_products':
        print(fc.show_bought())
    elif args.command == 'expired':
        print(fc.show_expired())
    elif args.command == 'revenue':
        print(fc.show_revenue())
    elif args.command == 'profit':
        print(fc.show_profit())
    elif args.command == 'advance_time':
        print(fc.advancetime())
    elif args.command == 'charity':
        print(fc.show_charity())
    main()
