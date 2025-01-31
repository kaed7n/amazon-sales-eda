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

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)
print(amazon_products.head(30))
