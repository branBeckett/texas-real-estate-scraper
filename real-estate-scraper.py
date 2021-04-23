#!/usr/bin/env python
# coding: utf-8

# ## Texas Real Estate Web Scraper
# 
# This web scraper was used for a site that contains Texas real estate, water district, and bond data. 

# In[1]:


import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import datetime as dt

har = requests.get("https://www.___.com/texasrealestate/waterdistricts") # Request webpage contents
soup = BeautifulSoup(har.content, 'html.parser')


# In[2]:


results = soup.find(id='highlist_tbl')
har_elems = results.find_all('div', class_='cell')

# Strip HTML data
result = []
for har_elem in har_elems:
    text = har_elem.get_text(strip = True)
    result.append(text)

final = list(result)


# In[3]:


# Creating separate lists for each column of data we want
district = []
county = []
tax_rate = []
tax_year = []
bonds_authorized = []
bonds_issued = []

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

# Adding the columns we created to our dataframe
data['District'] = district
data['County'] = county
data['Tax Rate'] = tax_rate
data['Tax Year'] = tax_year
data['Bonds Authorized'] = bonds_authorized
data['Bonds Issued'] = bonds_issued


# In[4]:


# Formatting the data and extracting data needed from the strings
columns_to_numeric = ['Bonds Authorized', 'Bonds Issued']

for col in columns_to_numeric:
    data[col] = data[col].str.extract(r"(\d*,*\d+,*\d+,*\d+,*)")
    data[col] = data[col].replace({',':''},regex=True).fillna(0).astype(int)
    
data['Tax Year'] = data['Tax Year'].str.extract(r"(\d+)").fillna(0)
data['Tax Year'] = data['Tax Year'].astype(int)

data['Tax Rate'] = data['Tax Rate'].str.extract(r"(\d+.\d+)").fillna(0)
data['Tax Rate'] = pd.to_numeric(data['Tax Rate'])

data['County'] = data['County'].str.extract(r"([^:]*$)")


# In[5]:


# Export to a csv with today's date
today = dt.datetime.today().strftime('%m%d%Y')  
output_file = 'har_data_{}.csv'.format(today)

data.to_csv(output_file, index=False)

