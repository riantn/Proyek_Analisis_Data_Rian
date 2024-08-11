#!/usr/bin/env python
# coding: utf-8

# # Proyek Analisis Data: Bike Sharing
# - **Nama:** Muhammad Rian Tirta Nugraha
# - **Email:** riantn0203@gmail.com
# - **ID Dicoding:** riantn

# ## Menentukan Pertanyaan Bisnis

# - Musim manakah dengan tingkat penyewaan sepeda tertinggi?
# - Bagaimana performa penyewaan sepeda tahun 2011 dan 2012?

# ## Import Semua Packages/Library yang Digunakan

# In[11]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ## Data Wrangling

# ### Gathering Data

# In[12]:


day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")


# ### Assessing Data

# Memeriksa data type

# In[13]:


#Memeriksa data type
day_df.info()
hour_df.info()


# Memeriksa data yang kosong

# In[14]:


#Memeriksa data yang kosong
day_df.isna().sum()
hour_df.isna().sum()


# Memeriksa data yang duplikasi

# In[15]:


#Memeriksa data yang duplikasi
print("Jumlah duplikasi data day: ", day_df.duplicated().sum())
print("Jumlah duplikasi data hour: ", hour_df.duplicated().sum())


# ### Cleaning Data

# Mengubah type data dteday menjadi datetime

# In[16]:


#Memperbaiki type data
datetime_columns = ["dteday"]

for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])
  hour_df[column] = pd.to_datetime(hour_df[column])


# In[17]:


hour_df.info()


# ## Exploratory Data Analysis (EDA)

# ##### Tampilan rangkuman parameter statistik

# In[18]:


hour_df.describe(include="all")


# In[19]:


day_df.describe(include="all")


# #### Penyewaan sepeda tertinggi dan terendah  (sum up casual and registered)

# In[20]:


print("Jumlah cnt paling tinggi: ",day_df.cnt.max())
print("Jumlah cnt paling rendah: ",day_df.cnt.min())


# #### Tanggal penyewaan sepeda tertinggi dan terendah

# In[21]:


highest_rent_byday = day_df.sort_values(by="cnt", ascending=False)[["dteday", "cnt"]]
highest_rent_byday.head(5)


# In[22]:


lowest_rent_byday = day_df.sort_values(by="cnt", ascending=True)[["dteday", "cnt"]]
lowest_rent_byday.head(5)


# #### Penyewaan sepeda tertinggi dan terendah berdasarkan musim

# In[23]:


day_df.groupby(by="season").agg({
    "registered" : ["max", "min"],
    "casual" : ["max", "min"],
    "cnt": ["max", "min"]
})


# #### Jumlah penyewaan sepeda berdasarkan musim tahun 2011

# In[24]:


#filter tahun 2011
year_2011_df = day_df[day_df['yr'] == 0]

season_rentals_2011 = year_2011_df.groupby('season')['cnt'].sum().reset_index()
season_rentals_2011['season'] = season_rentals_2011['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
season_rentals_2011.head()


# #### Jumlah penyewaan sepeda berdasarkan musim tahun 2012

# In[25]:


#filter tahun 2012
year_2012_df = day_df[day_df['yr'] == 1]

season_rentals_2012 = year_2012_df.groupby('season')['cnt'].sum().reset_index()
season_rentals_2012['season'] = season_rentals_2012['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
season_rentals_2012.head()


# In[26]:


season_rentals = day_df.groupby('season')['cnt'].sum().reset_index()
season_rentals['season'] = season_rentals['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
season_rentals.head()


# #### Jumlah penyewaan sepeda berdasarkan hari kerja dan hari libur/weekend

# In[27]:


workday_rentals = day_df.groupby('workingday')['cnt'].sum().reset_index()
workday_rentals['workingday'] = workday_rentals['workingday'].map({0: 'Holiday/Weekend', 1: 'Working Day'})
workday_rentals.head()


# #### Jumlah penyewaan sepeda tahun 2011 dalam setiap bulan

# In[28]:


#filter tahun 2011
year_2011_df = day_df[day_df['yr'] == 0]


month_rentals_2011 = year_2011_df.groupby('mnth')['cnt'].sum().reset_index()
month_rentals_2011.head(12)


# #### Jumlah penyewaan sepeda tahun 2012 dalam setiap bulan

# In[29]:


#filter tahun 2012
year_2012_df = day_df[day_df['yr'] == 1]


month_rentals_2012 = year_2012_df.groupby('mnth')['cnt'].sum().reset_index()
month_rentals_2012.head()


# #### Jumlah penyewaan sepeda 2011 vs 2012

# In[30]:


year_rentals = day_df.groupby('yr')['cnt'].sum().reset_index()
year_rentals['yr'] = year_rentals['yr'].map({0: '2011', 1: '2012'})
year_rentals.head()


# ## Visualization & Explanatory Analysis

# ### Pertanyaan 1:

# Musim manakah dengan tingkat penyewaan sepeda tertinggi?

# In[31]:


year_2011_df = day_df[day_df['yr'] == 0]
year_2012_df = day_df[day_df['yr'] == 1]

season_rentals_2011 = year_2011_df.groupby('season')['cnt'].sum().reset_index()
season_rentals_2011['season'] = season_rentals_2011['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

season_rentals_2012 = year_2012_df.groupby('season')['cnt'].sum().reset_index()
season_rentals_2012['season'] = season_rentals_2012['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y="cnt", x="season", data=season_rentals_2011.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Tahun 2011", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(y="cnt", x="season", data=season_rentals_2012.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Tahun 2012", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

plt.suptitle("Musim dengan penyewaan sepeda tertinggi", fontsize=20)
plt.show()



# ### Pertanyaan 2:

# #### **RFM analysis**
# *   Recency : date/hari terakhir dan total penyewaan sepeda tahun 2011 & 2012
# *   Frequency : bulan terakhir dengan total penyewaan sepeda tertinggi tahun 2011 & 2012
# *   Monetary : tahun dengan penyewaan sepeda tertinggi
# 
# 
# 
# 

# Bagaimana performa penyewaan sepeda tahun 2011 dan 2012?

# #####Recency tahun 2011, Frequency tahun 2011, dan perbandingan 2011 dan 2012

# In[32]:


# Recency
#filter tahun 2011
year_2011_df = day_df[day_df['yr'] == 0]
recent_days_2011 = year_2011_df.sort_values(by="dteday", ascending=False)[["dteday", "cnt"]].head()
recent_days_2011

# Frequency
#filter 4 bulan terakhir di tahun 2011
last_four_months_2011 = year_2011_df[(year_2011_df['mnth'] >= 9) & (year_2011_df['mnth'] <= 12)]

recent_months_2011 = last_four_months_2011[['mnth', 'cnt']].groupby("mnth").sum().reset_index()
recent_months_2011['mnth'] = recent_months_2011['mnth'].map({9: "Sept", 10: "Okt", 11: "Nov", 12: "Des"})
recent_months_2011

# Monetary
year_rentals = day_df.groupby('yr')['cnt'].sum().reset_index()
year_rentals['yr'] = year_rentals['yr'].map({0: '2011', 1: '2012'})
year_rentals


# In[33]:


fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Recency
sns.barplot(y="cnt", x="dteday", data=recent_days_2011.sort_values(by="dteday", ascending=True), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=15)
ax[0].tick_params(axis ='x', labelsize=15)

# Frequency
sns.barplot(y="cnt", x="mnth", data=recent_months_2011.sort_values(by="mnth", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency (months)", loc="center", fontsize=15)
ax[1].tick_params(axis='x', labelsize=15)

# Monetary
sns.barplot(y="cnt", x="yr", data=year_rentals.sort_values(by="yr", ascending=True), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary (years)", loc="center", fontsize=15)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Penyewaan Sepeda on RFM Parameters (Cnt)", fontsize=20)
plt.show()


# #####Recency tahun 2012, Frequency tahun 2012, dan perbandingan 2011 dan 2012

# In[34]:


# Recency
#filter tahun 2012
year_2012_df = day_df[day_df['yr'] == 1]
recent_days_2012 = year_2012_df.sort_values(by="dteday", ascending=False)[["dteday", "cnt"]].head()
recent_days_2012

# Frequency
#filter 4 bulan terakhir di tahun 2012
last_four_months_2012 = year_2012_df[(year_2012_df['mnth'] >= 9) & (year_2012_df['mnth'] <= 12)]

recent_months_2012 = last_four_months_2012[['mnth', 'cnt']].groupby("mnth").sum().reset_index()
recent_months_2012['mnth'] = recent_months_2012['mnth'].map({9: "Sept", 10: "Okt", 11: "Nov", 12: "Des"})
recent_months_2012

# Monetary
year_rentals = day_df.groupby('yr')['cnt'].sum().reset_index()
year_rentals['yr'] = year_rentals['yr'].map({0: '2011', 1: '2012'})
year_rentals


# In[35]:


fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Recency
sns.barplot(y="cnt", x="dteday", data=recent_days_2012.sort_values(by="dteday", ascending=True), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=15)
ax[0].tick_params(axis ='x', labelsize=15)

# Frequency
sns.barplot(y="cnt", x="mnth", data=recent_months_2012.sort_values(by="mnth", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency (months)", loc="center", fontsize=15)
ax[1].tick_params(axis='x', labelsize=15)

# Monetary
sns.barplot(y="cnt", x="yr", data=year_rentals.sort_values(by="yr", ascending=True), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary (years)", loc="center", fontsize=15)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Penyewaan Sepeda on RFM Parameters (Cnt)", fontsize=20)
plt.show()


# ## Conclusion

# - Conclution pertanyaan 1 :
# Musim gugur menjadi musim dengan penyewaan sepeda tertinggi
# 
# - Conclution pertanyaan 2 : Perfoma penyewaan sepeda setiap akhir bulan selalu menurun dan performa penyewaan sepeda mengalami peningkatan jika membandingkan tahun 2011 dan 2012
