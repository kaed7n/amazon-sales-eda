# Exploratory Data Analysis & Visualization for Amazon Products Sales Data
# By Kaedyn Crucickshank / Created 01/31/2025 / Last Modified -

# Import libraries
import pandas as pd
import zipfile
import matplotlib.pyplot as plt

# Read CSV zip into pandas dataframe

with zipfile.ZipFile("Amazon-Products.csv.zip") as zipref:
    with zipref.open(zipref.namelist()[0]) as z:
        amazon_products = pd.read_csv(z)

# Allow more output to be visible in terminal
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)

# Clean Data.

# remove extra index column
amazon_products.drop(columns=['Unnamed: 0'], inplace=True)

# Overview of data
print(amazon_products.isna().sum())
print(amazon_products.shape)
print("Data Overview Before\n\n")

# Working with just the products/rows that have ratings and discounted prices.
amazon_products.dropna(
    subset=['ratings', 'discount_price', 'actual_price'], inplace=True)

# Convert data types , remove $ and , from prices first
amazon_products['discount_price'] = amazon_products['discount_price'].str.replace(
    '₹', '').str.replace(',', '').str.strip()
amazon_products['actual_price'] = amazon_products['actual_price'].str.replace(
    '₹', '').str.replace(',', '').str.strip()

amazon_products['name'] = amazon_products['name'].astype('string')
amazon_products['main_category'] = amazon_products['main_category'].astype(
    'string')
amazon_products['sub_category'] = amazon_products['sub_category'].astype(
    'string')
amazon_products['ratings'] = pd.to_numeric(
    amazon_products['ratings'], errors='coerce')
amazon_products['discount_price'] = pd.to_numeric(
    amazon_products['discount_price'], errors='coerce')
amazon_products['actual_price'] = pd.to_numeric(
    amazon_products['actual_price'], errors='coerce')

# Drop rows with missing values (only some ratings, with 'get' instead of numerics for values)
amazon_products.dropna(inplace=True)

# Convert foreign currency (inr) to usd
conversion_rate = 0.013
amazon_products['discount_price'] = amazon_products['discount_price'] * \
    conversion_rate
amazon_products['actual_price'] = amazon_products['actual_price'] * \
    conversion_rate

# Data worked on
print(amazon_products.shape)
print(amazon_products.dtypes)
print("Data Overview After\n\n")
print(amazon_products.isna().sum())
