#!/usr/bin/env python
# coding: utf-8

# ## Texas Real Estate Web Scraper

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import datetime as dt

# Request webpage contents
har = requests.get("https://www._.com")
soup = BeautifulSoup(har.content, 'html.parser')

results = soup.find(id='highlist_tbl')
har_elems = results.find_all('div', class_='cell')

# Strip HTML data and return a single list of all real estate data found in the target table
result = []
for har_elem in har_elems:
    text = har_elem.get_text(strip = True)
    result.append(text)

final = list(result)

# Creating separate lists for each column of data we want
district = []
county = []
tax_rate = []
tax_year = []
bonds_authorized = []
bonds_issued = []

# Builds each column of data that will be used for the final dataframe
length = int((len(final) - 6) / 6) # To avoid range errors
i = 5
for string in range(length):
    district.append(final[i+1])
    county.append(final[i+2])
    tax_rate.append(final[i+3])
    tax_year.append(final[i+4])
    bonds_authorized.append(final[i+5])
    bonds_issued.append(final[i+6])
    i += 6

data = pd.DataFrame()

# Add each of the columns we created to the dataframe
data['District'] = district
data['County'] = county
data['Tax Rate'] = tax_rate
data['Tax Year'] = tax_year
data['Bonds Authorized'] = bonds_authorized
data['Bonds Issued'] = bonds_issued

# Formatting the data and extracting data needed from the strings
columns_to_numeric = ['Bonds Authorized', 'Bonds Issued']

for col in columns_to_numeric:
    data[col] = data[col].str.extract(r"(\d*,*\d+,*\d+,*\d+,*)")
    data[col] = data[col].replace({',':''},regex=True).fillna(0).astype(int)

# Clean and convert Tax Year to Integer Datatype
data['Tax Year'] = data['Tax Year'].str.extract(r"(\d+)").fillna(0)
data['Tax Year'] = data['Tax Year'].astype(int)

# Clean and convert Tax Rate column to numeric
data['Tax Rate'] = data['Tax Rate'].str.extract(r"(\d+.\d+)").fillna(0)
data['Tax Rate'] = pd.to_numeric(data['Tax Rate'])

data['County'] = data['County'].str.extract(r"([^:]*$)")

# Export formated dataframe to a csv with today's date as the filename
today = dt.datetime.today().strftime('%m%d%Y')
output_file = 'har_data_{}.csv'.format(today)

data.to_csv(output_file, index=False)
