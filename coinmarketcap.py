#!/usr/bin/env python

"""
coinmarketcap.py:  Script to download data from `CryptoCurrency Market Capitalizations` and filter for Ethereum data with a Market Cap.

Data is downloaded from https://coinmarketcap.com/assets/views/all/

10-17-2017 : Version 0.0.1
07-01-2017 : Created script
"""

__author__ = "Brad Luicas"
__copyright__ = "Copyright 2017, Brad Lucas"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brad Lucas"
__email__ = "brad@beaconhill.com"
__status__ = "Production"


import pandas as pd
import tabulate
from datetime import datetime

url = 'https://coinmarketcap.com/tokens/views/all/'

# Use Pandas to return first table on page
#
df = pd.read_html(url, attrs = {'id': 'assets-all'})[0]

# Original column names
#
# [ 0,    1,         2,          3,          4,         5,                   6,            7,        8,     9
# ['#', 'Name', 'Platform', 'Market Cap', 'Price', 'Circulating Supply', 'Volume (24h)', '% 1h', '% 24h', '% 7d']

# New column names
#
df.columns = ['#', 'Name', 'Platform', 'MarketCap', 'Price', 'Supply', 'VolumeDay', 'pctHour', 'pctDay', 'pctWeek']


# Build an upper case name column so we can sort on it more easily
#
df['NameUpper'] = map(lambda x: x.upper(), df['Name'])


# Clean the data with 'numbers' by removing $, % and , characters
#
df['Price'] = df['Price'].str.replace('$', '')
df['MarketCap'] = df['MarketCap'].str.replace('$', '')
df['MarketCap'] = df['MarketCap'].str.replace(',', '')
df['VolumeDay'] = df['VolumeDay'].str.replace('$', '')
df['VolumeDay'] = df['VolumeDay'].str.replace(',', '')
df['VolumeDay'] = df['VolumeDay'].str.replace('Low Vol', '0')
df['pctHour'] = df['pctHour'].str.replace('%', '')
df['pctDay'] = df['pctDay'].str.replace('%', '')
df['pctWeek'] = df['pctWeek'].str.replace('%', '')


# Filter so we only have rows which are Ethereum and which have a value for Market Cap
#
df = df.loc[(df['Platform'] == 'Ethereum') & (df['MarketCap'] != '?')]


# Covert 'number' columns to numeric type so they will sort as we'd like
#
def coerce_df_columns_to_numeric(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, errors='coerce')


coerce_df_columns_to_numeric(df, ['MarketCap', 'Price', 'Supply', 'VolumeDay', 'pctHour', 'pctDay', 'pctWeek'])


# Functions to return dataframe sorted in some fashion
#
def sort_dataframe(df, col, ascending=True):
    return df.sort_values([col], ascending=ascending)


def sort_name(df):
    return sort_dataframe(df, 'NameUpper', True).ix[:, [1, 3, 4, 5, 6]]


def sort_marketcap(df):
    return sort_dataframe(df, 'MarketCap', False).ix[:, [1, 3]]


def sort_price(df):
    return sort_dataframe(df, 'Price', False).ix[:, [1, 4]]


def sort_volume(df):
    return sort_dataframe(df, 'VolumeDay', False).ix[:, [1, 6]]


def sort_hour(df):
    return sort_dataframe(df, 'pctHour', False).ix[:, [1, 7]]


def sort_day(df):
    return sort_dataframe(df, 'pctDay', False).ix[:, [1, 8]]


def sort_week(df):
    return sort_dataframe(df, 'pctWeek', False).ix[:, [1, 9]]


# Print sorted versions of the dataframe in a tabulated form
#
def print_tabulated(df):
    print tabulate.tabulate(df, headers='keys', showindex='false', numalign="right")


def report():
    print "Title  : " + "CryptoAsset Market Capitalizations"
    print "       : " + "Etheruem with Market Cap"
    print "Source : " + url
    print "Time   : " + str(datetime.now().strftime("%Y-%m-%d %H:%M"))
    print ""
    print ""
    print_tabulated(sort_name(df))
    print ""
    print_tabulated(sort_marketcap(df))
    print ""
    print_tabulated(sort_price(df))
    print ""
    print_tabulated(sort_volume(df))
    print ""
    print_tabulated(sort_hour(df))
    print ""
    print_tabulated(sort_day(df))
    print ""
    print_tabulated(sort_week(df))


if __name__ == '__main__':
    report()
