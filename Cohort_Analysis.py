import pandas as pd
import datetime as dt
online=pd.read_csv("online.csv")
online['InvoiceDate'] = pd.to_datetime(online['InvoiceDate'])


# Define a function that will parse the date
def get_month(x):
    return dt.datetime(x.year, x.month, 1)


# Create InvoiceDay column
online['InvoiceMonth'] = online['InvoiceDate'].apply(get_month)


# Group by CustomerID and select the InvoiceDay value
grouping = online.groupby('CustomerID')['InvoiceMonth']

# Assign a minimum InvoiceDay value to the dataset
online['CohortMonth'] = grouping.transform('min')
#print(online.head())


def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day


# Get the integers for date parts from the `InvoiceDay` column
invoice_year, invoice_month, invoice_day = get_date_int(online, "InvoiceMonth")

# Get the integers for date parts from the `CohortDay` column
cohort_year, cohort_month, cohort_day = get_date_int(online, "CohortMonth")

# Calculate difference in years
years_diff = invoice_year - cohort_year

# Calculate difference in months
months_diff = invoice_month - cohort_month

# Extract the difference in days from all previous values
online['CohortIndex'] = years_diff * 12 + months_diff + 1


def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day


# Count the number of unique values per customer ID
grouping = online.groupby(["CohortMonth", "CohortIndex"])
cohort_data = grouping["CustomerID"].apply(pd.Series.nunique).reset_index()


# Create a pivot
cohort_counts = cohort_data.pivot(index="CohortMonth",
                                  columns="CohortIndex",
                                  values="CustomerID")
print(cohort_counts)

# Select the first column and store it to cohort_sizes
cohort_sizes = cohort_counts.iloc[:,0]

# Divide the cohort count by cohort sizes along the rows
retention = cohort_counts.divide(cohort_sizes, axis=0)
retention.round(3)*100
print(retention)

# Create a groupby object and pass the monthly cohort and cohort index as a list
grouping = online.groupby(["CohortMonth", "CohortIndex"])

# Calculate the average of the Quantity column
cohort_data = grouping["Quantity"].mean()

# Reset the index of cohort_data
cohort_data = cohort_data.reset_index()

# Create a pivot
average_quantity = cohort_data.pivot(index="CohortMonth",
                                     columns="CohortIndex",
                                     values="Quantity")
print(average_quantity.round(1))

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(12,10))
plt.title("Retention Rates")
sns.heatmap(data=retention
            ,annot=True
            ,fmt=".0%"
            ,vmin=0.0
            ,vmax=0.5
            ,cmap="YlGnBu")

plt.show()
