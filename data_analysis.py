'''
Exploratory Data Analysis and Visualization for Amazon Products Sales Data
By Kaedyn Crucickshank / Created 01/31/2025 / Last Modified -
'''

# Import libraries
import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import numpy as np
import json

# Read CSV zip into pandas dataframe
with zipfile.ZipFile("Amazon-Products.csv.zip") as zipref:
    with zipref.open(zipref.namelist()[0]) as z:
        amazon_products = pd.read_csv(z)

# Allow more output to be visible in terminal
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)


# (1)
# Clean Data.
# # # # # # #

# remove extra index column
amazon_products.drop(columns=['Unnamed: 0'], inplace=True)

# data to clean
print(f'\n\n\n{amazon_products.shape}')
print(amazon_products.isna().sum())
print("Before Cleaning\n\n")

# Working with just the products/rows that have ratings and discounted prices.
amazon_products.dropna(
    subset=['ratings', 'actual_price'], inplace=True)

# Remove $ and , from prices
amazon_products['discount_price'] = amazon_products['discount_price'].str.replace(
    '₹', '').str.replace(',', '').str.strip()
amazon_products['actual_price'] = amazon_products['actual_price'].str.replace(
    '₹', '').str.replace(',', '').str.strip()

# Convert data types
amazon_products['name'] = amazon_products['name'].astype('string')
amazon_products['main_category'] = amazon_products['main_category'].astype(
    'string')
amazon_products['sub_category'] = amazon_products['sub_category'].astype(
    'string')
amazon_products['ratings'] = pd.to_numeric(
    amazon_products['ratings'], errors='coerce')
amazon_products['no_of_ratings'] = pd.to_numeric(
    amazon_products['no_of_ratings'], errors='coerce')
amazon_products['discount_price'] = pd.to_numeric(
    amazon_products['discount_price'], errors='coerce')
amazon_products['actual_price'] = pd.to_numeric(
    amazon_products['actual_price'], errors='coerce')

# Drop rows with missing values (NaN rows in price & ratings w/ values 'get' instead of numerics)
amazon_products.dropna(
    subset=['ratings', 'no_of_ratings', 'actual_price'], inplace=True)

# Convert foreign currency (inr) to usd
conversion_rate = 0.013
amazon_products['discount_price'] = (
    amazon_products['discount_price'] * conversion_rate).round(2)
amazon_products['actual_price'] = amazon_products['actual_price'] * \
    conversion_rate

# data being manipulated/explored
print(amazon_products.shape)
print(amazon_products.dtypes)
print("Data Overview After\n\n")


# (2)
# Exploratory Data Analysis.
# # # # # # # # # # # # # # #

# basic metrics
total_products = amazon_products.shape[0]
avg_rating = float(amazon_products['ratings'].mean())
percent_discounted = round((amazon_products['discount_price'].notna(
).sum() / total_products) / 100, 2)
average_discount_percent = (
    (amazon_products['actual_price'] - amazon_products['discount_price']) / amazon_products['actual_price']).dropna().mean()

# key metrics
highest_rated_sub_category = amazon_products.groupby(
    'sub_category')['ratings'].mean().idxmax()
highest_rated_main_category = amazon_products.groupby(
    'main_category')['ratings'].mean().idxmax()
highest_rated_products = amazon_products.nlargest(10, ['ratings', 'no_of_ratings'])[
    ['name', 'ratings', 'no_of_ratings']]

print(f"Total Products: {total_products}")
print(f"Average Rating: {avg_rating:.2f}")
print(f"Percent of Products Discounted: {percent_discounted:.2%}")
print(f"Average Discount Percent: {average_discount_percent:.2%}")
print(f"\nTop 10 Rated Products:\n{highest_rated_products}")


# (3) Exploration and Visualization.
# # # # # # # # # # # # # # # # # # #

# Distribution of Ratings (Fig 1)
plt.hist(amazon_products['ratings'], bins=10,
         color='lightblue', edgecolor='black', linewidth=1.3)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Product Count')
plt.show()

# filter extremes for price trends
removed_nan_discount = amazon_products.dropna(subset=['discount_price'])
price_no_extremes = removed_nan_discount['actual_price'].quantile(0.98)
filtered_prices = removed_nan_discount[removed_nan_discount['actual_price']
                                       <= price_no_extremes]

# hexbin plot of actual price, frequency / density of discount price (Fig 2)
plt.figure(figsize=(10, 6))
hb = plt.hexbin(filtered_prices['actual_price'],
                filtered_prices['discount_price'], gridsize=100, bins='log', cmap='viridis', mincnt=1, vmin=0.999, vmax=200)
plt.colorbar(hb, label='Density').ax.yaxis.label.set_color('red')
plt.plot([0, price_no_extremes], [0, price_no_extremes],
         color='magenta', linestyle='--', label='Actual Price')
# discount price trend line
ap_dp = np.polyfit(filtered_prices['actual_price'],
                   filtered_prices['discount_price'], 1)
ap_dp_1d = np.poly1d(ap_dp)
plt.plot(filtered_prices['actual_price'], ap_dp_1d(
    filtered_prices['actual_price']), color='red', label='Discount Price Trend')

plt.title('Price Trends of Amazon Products\n(prices coverted to $USD)', color='blue')
plt.xlabel('Actual Price', color='magenta')
plt.ylabel('Discount Price', color='red')
plt.legend()
plt.grid(True)
plt.show()

# (3a)
# Correlation between Ratings and Discount Percentage.
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# products w/ highest discount percentages
amazon_products['discount_percent'] = round(((
    (amazon_products['actual_price'] - amazon_products['discount_price']) / amazon_products['actual_price']) * 100), 2)
# top 10 from highest discount percentage
highest_discount_percent = amazon_products.nlargest(10, 'discount_percent')[
    ['name', 'discount_percent', 'actual_price', 'discount_price']]
print(f"Top 10 Products with Highest Discount Percentages:\n{
      highest_discount_percent}")

# plot correlation (Fig 3)
plt.figure(figsize=(10, 6))
rating_v_discount = plt.hexbin(amazon_products['ratings'],
                               amazon_products['discount_percent'], gridsize=50, cmap='viridis', mincnt=1, vmin=1, vmax=1000)
plt.colorbar(rating_v_discount,
             label='Density').ax.yaxis.label.set_color('red')
plt.title('Ratings vs Discount Percentage')
plt.xlabel('Ratings', color='blue')
plt.ylabel('Discount Percentage', color='lightgreen')
plt.grid(True, alpha=0.3)
plt.show()

# saving data for power bi dashboard

# new dataframe with discount percent
filtered_prices['discount_percent'] = (
    (filtered_prices['actual_price'] - filtered_prices['discount_price']
     ) / filtered_prices['actual_price'] * 100
).round(2)
# important metrics
metrics = {
    "total_products": total_products,
    "avg_discount_percent": average_discount_percent,
    "percent_discounted": percent_discounted * 100,
    "avg_rating": avg_rating,
    "highest_rated_category": highest_rated_main_category,
    "highest_rated_subcategory": highest_rated_sub_category,
    "highest_rated_products": highest_rated_products.to_dict('records')
}

with open('metrics.json', 'w') as file:
    json.dump(metrics, file)
filtered_prices.to_csv('filtered_prices.csv', index=False)
