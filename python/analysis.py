import pandas as pd


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_excel("Online Retail.xlsx")

print("\n========== DATASET OVERVIEW ==========")

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATASET INFO ---")
df.info()

print("\n--- STATISTICAL SUMMARY ---")
print(df.describe())


# ============================================================
# 2. DATA QUALITY CHECKS
# ============================================================

print("\n========== DATA QUALITY CHECKS ==========")

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- CANCELLED ORDERS ---")
cancelled_orders = df['InvoiceNo'].astype(str).str.startswith('C').sum()
print(cancelled_orders)

print("\n--- DUPLICATE ROWS ---")
duplicate_count = df.duplicated().sum()
print("Duplicate rows:", duplicate_count)

duplicate_percentage = (duplicate_count / len(df)) * 100
print("Duplicate percentage:", duplicate_percentage)

print("\n--- NEGATIVE QUANTITY ---")
negative_quantity = (df['Quantity'] < 0).sum()
print(negative_quantity)

print("\n--- NON-POSITIVE UNIT PRICE ---")
non_positive_price = (df['UnitPrice'] <= 0).sum()
print(non_positive_price)

print("\n--- NON-POSITIVE PRICE RECORDS ---")
print(
    df[df['UnitPrice'] <= 0][
        ['InvoiceNo', 'StockCode', 'Description',
         'Quantity', 'UnitPrice', 'CustomerID']
    ].head(20)
)

print("\n--- NEGATIVE UNIT PRICE ---")
negative_price = (df['UnitPrice'] < 0).sum()
print(negative_price)


# ============================================================
# 3. DATA CLEANING
# ============================================================

print("\n========== DATA CLEANING ==========")

clean_df = df.copy()

# Remove duplicate rows
clean_df = clean_df.drop_duplicates()

# Remove cancelled transactions
clean_df = clean_df[
    ~clean_df['InvoiceNo'].astype(str).str.startswith('C')
]

# Keep only positive quantities
clean_df = clean_df[clean_df['Quantity'] > 0]

# Keep only positive prices
clean_df = clean_df[clean_df['UnitPrice'] > 0]

print("\n--- CLEAN DATASET ---")
print("Original rows:", len(df))
print("Clean rows:", len(clean_df))
print("Rows removed:", len(df) - len(clean_df))


# ============================================================
# 4. CREATE REVENUE
# ============================================================

clean_df['Revenue'] = (
    clean_df['Quantity'] * clean_df['UnitPrice']
)

print("\n--- REVENUE ---")
print(
    clean_df[
        ['Quantity', 'UnitPrice', 'Revenue']
    ].head()
)


# ============================================================
# 5. BASIC SALES KPIs
# ============================================================

total_revenue = clean_df['Revenue'].sum()
total_quantity = clean_df['Quantity'].sum()
total_orders = clean_df['InvoiceNo'].nunique()
total_customers = clean_df['CustomerID'].nunique()

print("\n========== BASIC SALES METRICS ==========")

print("Total Revenue:", total_revenue)
print("Total Quantity Sold:", total_quantity)
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)


# ============================================================
# 6. AVERAGE ORDER VALUE
# ============================================================

average_order_value = total_revenue / total_orders

print("\n--- AVERAGE ORDER VALUE ---")
print("Average Order Value:", average_order_value)


# ============================================================
# 7. MONTHLY SALES ANALYSIS
# ============================================================

clean_df['InvoiceDate'] = pd.to_datetime(
    clean_df['InvoiceDate']
)

clean_df['YearMonth'] = (
    clean_df['InvoiceDate']
    .dt.to_period('M')
)

monthly_sales = (
    clean_df
    .groupby('YearMonth')['Revenue']
    .sum()
    .sort_index()
)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales)


# Highest revenue month
highest_month = monthly_sales.idxmax()
highest_month_revenue = monthly_sales.max()

print("\n--- HIGHEST REVENUE MONTH ---")
print("Month:", highest_month)
print("Revenue:", highest_month_revenue)


# ============================================================
# 8. COUNTRY-WISE SALES ANALYSIS
# ============================================================

country_sales = (
    clean_df
    .groupby('Country')['Revenue']
    .sum()
    .sort_values(ascending=False)
)

print("\n========== COUNTRY-WISE SALES ==========")
print(country_sales.head(10))


# Highest revenue country
top_country = country_sales.idxmax()
top_country_revenue = country_sales.max()

print("\n--- TOP COUNTRY ---")
print("Country:", top_country)
print("Revenue:", top_country_revenue)


# ============================================================
# 9. TOP 10 PRODUCTS BY REVENUE
# ============================================================

product_sales = (
    clean_df
    .groupby('Description')['Revenue']
    .sum()
    .sort_values(ascending=False)
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")
print(product_sales.head(10))


# ============================================================
# 10. TOP 10 PRODUCTS BY QUANTITY
# ============================================================

product_quantity = (
    clean_df
    .groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
)

print("\n========== TOP 10 PRODUCTS BY QUANTITY ==========")
print(product_quantity.head(10))


# ============================================================
# 11. TOP 10 CUSTOMERS BY REVENUE
# ============================================================

customer_sales = (
    clean_df
    .dropna(subset=['CustomerID'])
    .groupby('CustomerID')['Revenue']
    .sum()
    .sort_values(ascending=False)
)

print("\n========== TOP 10 CUSTOMERS BY REVENUE ==========")
print(customer_sales.head(10))


# ============================================================
# 12. CUSTOMER ORDER ANALYSIS
# ============================================================

customer_orders = (
    clean_df
    .dropna(subset=['CustomerID'])
    .groupby('CustomerID')['InvoiceNo']
    .nunique()
    .sort_values(ascending=False)
)

print("\n========== TOP 10 CUSTOMERS BY NUMBER OF ORDERS ==========")
print(customer_orders.head(10))


# ============================================================
# 13. SAVE CLEAN DATASET
# ============================================================

clean_df.to_csv(
    "clean_online_retail.csv",
    index=False
)

print("\n========== PROJECT COMPLETE ==========")
print("Clean dataset saved as: clean_online_retail.csv")

import matplotlib.pyplot as plt


# ============================================================
# 14. DATA VISUALIZATION
# ============================================================

# 1. Monthly Revenue Trend
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker='o'
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Top 10 Countries by Revenue
top_countries = country_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_countries.index,
    top_countries.values
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


# 3. Top 10 Products by Revenue
top_products = product_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_products.index,
    top_products.values
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.show()


# 4. Top 10 Products by Quantity
top_quantity_products = product_quantity.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_quantity_products.index,
    top_quantity_products.values
)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.tight_layout()
plt.show()


# 5. Top 10 Customers by Revenue
top_customers = customer_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_customers.index.astype(str),
    top_customers.values
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.show()

# ============================================================
# 14. DATA VISUALIZATION
# ============================================================

import matplotlib.pyplot as plt


# 1. Monthly Revenue Trend
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker='o'
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("monthly_revenue.png")
plt.show()
plt.close()


# 2. Top 10 Countries by Revenue
top_countries = country_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_countries.index,
    top_countries.values
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig("top_countries_revenue.png")
plt.show()
plt.close()


# 3. Top 10 Products by Revenue
top_products = product_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_products.index,
    top_products.values
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig("top_products_revenue.png")
plt.show()
plt.close()


# 4. Top 10 Products by Quantity
top_quantity_products = product_quantity.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_quantity_products.index,
    top_quantity_products.values
)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig("top_products_quantity.png")
plt.show()
plt.close()


# 5. Top 10 Customers by Revenue
top_customers = customer_sales.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(
    top_customers.index.astype(str),
    top_customers.values
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Customer ID")
plt.tight_layout()

plt.savefig("top_customers_revenue.png")
plt.show()
plt.close()


print("\n========== CHARTS SAVED ==========")
print("1. monthly_revenue.png")
print("2. top_countries_revenue.png")
print("3. top_products_revenue.png")
print("4. top_products_quantity.png")
print("5. top_customers_revenue.png")
