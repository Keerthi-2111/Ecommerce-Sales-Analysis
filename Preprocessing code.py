import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# ----------------------------------------------------------
# DATABASE CONNECTION
# ----------------------------------------------------------

engine = create_engine(
    "mysql+pymysql://root:Keerthi%402004@localhost/ecommerce"
)

df = pd.read_sql(
    "SELECT * FROM ecommerce_sales",
    engine
)

# ----------------------------------------------------------
# FIRST 5 RECORDS
# ----------------------------------------------------------

print("\nFIRST 5 RECORDS")
print(df.head())

# ----------------------------------------------------------
# LAST 5 RECORDS
# ----------------------------------------------------------

print("\nLAST 5 RECORDS")
print(df.tail())

# ----------------------------------------------------------
# SHAPE
# ----------------------------------------------------------

print("\nDATASET SHAPE")
print(df.shape)

print(f"Rows : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# ----------------------------------------------------------
# COLUMN NAMES
# ----------------------------------------------------------

print("\nCOLUMN NAMES")
print(df.columns.tolist())

# ----------------------------------------------------------
# DATA TYPES
# ----------------------------------------------------------

print("\nDATA TYPES")
print(df.dtypes)

# ----------------------------------------------------------
# DATASET INFO
# ----------------------------------------------------------

print("\nDATASET INFO")
df.info()

# ----------------------------------------------------------
# DESCRIPTIVE STATISTICS
# ----------------------------------------------------------

print("\nSTATISTICAL SUMMARY")
print(df.describe())

# ----------------------------------------------------------
# MISSING VALUES
# ----------------------------------------------------------

print("\nMISSING VALUES")
print(df.isnull().sum())

# ----------------------------------------------------------
# DUPLICATE RECORDS
# ----------------------------------------------------------

print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# ----------------------------------------------------------
# DATE CONVERSION
# ----------------------------------------------------------

if 'Order_Date' in df.columns:
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month
    df['Month_Name'] = df['Order_Date'].dt.month_name()
    df['Day'] = df['Order_Date'].dt.day

# ----------------------------------------------------------
# PROFIT MARGIN
# ----------------------------------------------------------

if 'Profit' in df.columns and 'Sales' in df.columns:
    df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

print("\nFEATURE ENGINEERING COMPLETED")

# ----------------------------------------------------------
# UNIQUE VALUES
# ----------------------------------------------------------

if 'Category' in df.columns:
    print("\nUNIQUE CATEGORIES")
    print(df['Category'].unique())

if 'Region' in df.columns:
    print("\nUNIQUE REGIONS")
    print(df['Region'].unique())

# ----------------------------------------------------------
# SALES DISTRIBUTION
# ----------------------------------------------------------

if 'Sales' in df.columns:
    plt.figure(figsize=(8, 5))
    plt.hist(df['Sales'], bins=20)
    plt.title("Sales Distribution")
    plt.xlabel("Sales")
    plt.ylabel("Frequency")
    plt.show()

# ----------------------------------------------------------
# PROFIT DISTRIBUTION
# ----------------------------------------------------------

if 'Profit' in df.columns:
    plt.figure(figsize=(8, 5))
    plt.hist(df['Profit'], bins=20)
    plt.title("Profit Distribution")
    plt.xlabel("Profit")
    plt.ylabel("Frequency")
    plt.show()

# ----------------------------------------------------------
# CATEGORY-WISE SALES
# ----------------------------------------------------------

if 'Category' in df.columns and 'Sales' in df.columns:

    category_sales = (
        df.groupby('Category')['Sales']
        .sum()
        .sort_values(ascending=False)
    )

    print("\nCATEGORY SALES")
    print(category_sales)

    plt.figure(figsize=(8, 5))
    category_sales.plot(kind='bar')
    plt.title("Category Wise Sales")
    plt.ylabel("Sales")
    plt.show()

# ----------------------------------------------------------
# REGION-WISE PROFIT
# ----------------------------------------------------------

if 'Region' in df.columns and 'Profit' in df.columns:

    region_profit = (
        df.groupby('Region')['Profit']
        .sum()
        .sort_values(ascending=False)
    )

    print("\nREGION PROFIT")
    print(region_profit)

    plt.figure(figsize=(8, 5))
    region_profit.plot(kind='bar')
    plt.title("Region Wise Profit")
    plt.ylabel("Profit")
    plt.show()

# ----------------------------------------------------------
# TOP PRODUCTS
# ----------------------------------------------------------

if 'Product_Name' in df.columns and 'Sales' in df.columns:

    top_products = (
        df.groupby('Product_Name')['Sales']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTOP PRODUCTS")
    print(top_products)

    plt.figure(figsize=(10, 5))
    top_products.plot(kind='bar')
    plt.title("Top 10 Products")
    plt.ylabel("Sales")
    plt.show()

# ----------------------------------------------------------
# MONTHLY SALES TREND
# ----------------------------------------------------------

if 'Year' in df.columns and 'Month_Name' in df.columns:

    monthly_sales = (
        df.groupby(['Year', 'Month_Name'])['Sales']
        .sum()
        .reset_index()
    )

    print("\nMONTHLY SALES TREND")
    print(monthly_sales)

# ----------------------------------------------------------
# CORRELATION MATRIX
# ----------------------------------------------------------

numeric_df = df.select_dtypes(include=np.number)

corr_matrix = numeric_df.corr()

print("\nCORRELATION MATRIX")
print(corr_matrix)

plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True)
plt.title("Correlation Heatmap")
plt.show()

# ----------------------------------------------------------
# OUTLIERS
# ----------------------------------------------------------

if 'Sales' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['Sales'])
    plt.title("Sales Outliers")
    plt.show()

if 'Profit' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['Profit'])
    plt.title("Profit Outliers")
    plt.show()

# ----------------------------------------------------------
# SAVE CLEANED DATA
# ----------------------------------------------------------

df.to_csv("ecommerce_sales_cleaned.csv", index=False)

print("\n✅ Cleaned Dataset Saved Successfully")
# df.to_csv("ecommerce_sales_cleaned.csv", index=False)

df.to_sql(
    name='ecommerce_sales_cleaned',
    con=engine,
    if_exists='replace',
    index=False
)

print("✅ Cleaned dataset stored in MySQL successfully!")
