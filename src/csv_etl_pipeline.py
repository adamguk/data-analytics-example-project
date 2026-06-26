from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from functions.snowflake_utils import load_data_to_snowflake
# ======================= HEADER =======================  

# ======================= SOURCE FILE ======================= 
# Location of the CSV file. Original file source: https://www.kaggle.com/datasets/kpatel123/ecommerce-online-sales-records
# License CC0: Public Domain
# File Version 1.0
# Include "r" to tell VS this is all a raw string - avoids slash errors from misinterpritation
file_fact_sales = Path(r"C:\Users\Public\Documents\ecommerce_sales_1000_records.csv")
file_dimension_categories = Path(r"C:\Users\Public\Documents\dimension_product_table.csv")
#region ======================= DATAFRAME POPULATION ======================= 
# Read CSV into Dataframe
df_sales = pd.read_csv(file_fact_sales)
df_categories = pd.read_csv(file_dimension_categories)
#endregion

#region ======================= DATAFRAME QUALITY EVALUATION ======================= 

# Print to log to view previews of the dataframe
print("===HEAD: FIRST FEW ROWS===")
print(df_sales.head(),"\n")
print("===TAIL: LAST FEW ROWS===")
print(df_sales.tail(),"\n")
print("===SHAPE: ROW & COLUMN COUNT===")
print("Shape:",df_sales.shape,"\n")
print("===COLUMNS: LIST OF COLUMNS===")
print("Columns:",df_sales.columns.to_list(),"\n")
print("===INFO: COLUMN TYPES & NULL COUNTS===")
print(df_sales.info())
print("===DESCRIBE: STATS FOR ALL COLUMNS===")
print(df_sales.describe(include='all'),"\n")
#endregion

#region ======================= DATAFRAME CLEANING ======================= 
# Remove any completely empty rows or columns.
df_sales = df_sales.dropna(how="all")
df_categories = df_categories.dropna(how="all")

# Remove Category column as its missing values. We will replace this later using the master product dimension table
df_sales = df_sales.drop(columns="Category")

# Fill some missing values. Could be done one line of code per column, but this is less code for the same result
na_replacements = {"City":"No City Defined","Product":"No Product Defined"}
df_sales = df_sales.fillna(value=na_replacements)

# Add our placeholder into the Category dataframe as a new row at the bottom. 
df_categories.loc[len(df_categories)] = {'Product':'No Product Defined','Category':'Uncategorised'}

# Some Products dont have a Category. Join to categories dimension table to fill based on Product
df_sales = df_sales.merge(
    df_categories,
    how='left',
    on='Product'
)

print(df_sales.info())
#endregion

# Calculate revenue
df_sales['Revenue'] = df_sales['Price'] * df_sales['Quantity'] 

# Add Reporting date to 1st of month
df_sales['Date'] = pd.to_datetime(df_sales['Date'],dayfirst=True)
df_sales['Reporting Date'] = df_sales['Date'].dt.to_period('M').dt.to_timestamp()

load_data_to_snowflake(df_sales, "FACT_SALES")


