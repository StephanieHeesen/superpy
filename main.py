# Imports
import argparse
import csv
from datetime import date
import pandas as pd

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass

#start van command line tool
parser = argparse.ArgumentParser(prog= 'superpy', description='Inventory system')
subparser = parser.add_subparsers(dest='command')

# command line to add a bought product.
buy = subparser.add_parser('buy')
buy.add_argument('-product_name', type=str, help='name of the product')
buy.add_argument('-buy_price', type=float, help='price paid for 1 product')
buy.add_argument('-quantity', type=int, help= 'amount of bought products')
buy.add_argument('-expiration_date', type=str, help='dat in yyyy-mm-dd when product expired')

# command line to show inventory
inventory = subparser.add_parser('inventory')
inventory.add_argument('time inventory', type=str, help='now or yesterday')

# command line to sell a product.
sell = subparser.add_parser('sell')
sell.add_argument('product_name', type=str, help= 'name of the product')
sell.add_argument('sell_price', type=float, help= 'price for 1 sold product')
sell.add_argument('quantity', type=int, help= 'amount of sold products')

# command line to show sold and expired products.
sold_products = subparser.add_parser('sold_products')

args = parser.parse_args()


#open en show csv files
def all_bought():
    with open('superpy/bought.csv', newline='') as csvfile:
        bought_file = csv.reader(csvfile, delimiter=' ', quotechar=' ')
        for row in bought_file:
            print(' '.join(row))

def all_sold():
    with open('superpy/sold.csv', newline='') as file:
        sold_file = csv.reader(file)
        for row in sold_file:
            print(' '.join(row))


#write csv files
def append_new_product():
    with open('superpy/bought.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        # making an ID
        rowcount  = 0
        for row in open("superpy/bought.csv"):
            rowcount+= 1
        # Add contents of list as last row in the csv file
        csv_writer.writerow([rowcount, args.product_name, args.buy_price, args.quantity, args.expiration_date])
        # Add new products to instock file
        with open('superpy/instock.csv', 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow([rowcount, args.product_name, args.quantity, args.expiration_date])
            return 'OK'
            
def sold_product():
    with open('superpy/sold.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        # making an ID
        rowcount  = 0
        for row in open("superpy/sold.csv"):
            rowcount+= 1
        # Add contents as last row in the csv file    
        csv_writer.writerow([rowcount, args.product_name, args.sell_price, args.quantity])
        return 'OK'

def link_buy_sold():
    # search and take product from instock csv file
        for row in open('superpy/instock.csv'):
            if args.product_name in row:
                return row

def change_quanity():
    try:
        df = pd.read_csv('superpy/instock.csv', index_col='product_name')
        df.loc[args.product_name, 'quantity'] = (df.loc[args.product_name, 'quantity'] -args.quantity)
        # Write DataFrame to CSV file
        df.to_csv('superpy/instock.csv')
    except KeyError:
        print ('This product is not in stock')
    return 

if __name__ == "__main__":
    if args.command == 'inventory':
        print(all_bought())
    elif args.command == 'buy':
        print(append_new_product())
    elif args.command == 'sell':
        print(sold_product())
        print(change_quanity())
    elif args.command == 'sold_products':
        print(all_sold())
    main()
