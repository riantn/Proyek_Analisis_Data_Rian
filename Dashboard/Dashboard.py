import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='white')

day_df = pd.read_csv("day.csv")

# Define by tahun
year_2011_df = day_df[day_df['yr'] == 0]
year_2012_df = day_df[day_df['yr'] == 1]

# Define by bulan
month_2011_df = year_2011_df[['mnth', 'cnt']].groupby("mnth").sum().reset_index()
month_2012_df = year_2012_df[['mnth', 'cnt']].groupby("mnth").sum().reset_index()

# Define by season
season_rentals_2011 = year_2011_df.groupby('season')['cnt'].sum().reset_index()
season_rentals_2011['season'] = season_rentals_2011['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

season_rentals_2012 = year_2012_df.groupby('season')['cnt'].sum().reset_index()
season_rentals_2012['season'] = season_rentals_2012['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Define total Fall
fall_2011 = season_rentals_2011[season_rentals_2011['season'] == 'Fall']
fall_2012 = season_rentals_2012[season_rentals_2011['season'] == 'Fall']


st.subheader('Best Season for Rental Bikes')

col1, spacer, col2 = st.columns([1, 0.1, 1])

with col1:
    total_rental_2011 = year_2011_df.cnt.sum()
    st.metric("Total Rental Bikes 2011", value=total_rental_2011)

    total_rental_fall_2011 = fall_2011.cnt
    st.metric("Fall Season", value=total_rental_fall_2011)

with col2:
    total_rental_2012 = year_2012_df.cnt.sum()
    st.metric("Total Rental Bikes 2012", value=total_rental_2012)

    total_rental_fall_2012 = fall_2012.cnt
    st.metric("Fall Season", value=total_rental_fall_2012)


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y="cnt", x="season", data=season_rentals_2011.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Season 2011", loc="center", fontsize=25)
ax[0].tick_params(axis ='x', labelsize=20)
ax[0].tick_params(axis='y', labelsize=20)

sns.barplot(y="cnt", x="season", data=season_rentals_2012.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Best Season 2012", loc="center", fontsize=25)
ax[1].tick_params(axis='x', labelsize=20)
ax[1].tick_params(axis='y', labelsize=20)

st.pyplot(fig)

st.markdown("<br>", unsafe_allow_html=True)  

# Define by tahun 2012
year_2012_df = day_df[day_df['yr'] == 1]
# Define by bulan
month_2012_df = year_2012_df[['mnth', 'cnt']].groupby("mnth").sum().reset_index()


# Recency
recent_days_2012 = year_2012_df.sort_values(by="dteday", ascending=False)[["dteday", "cnt"]].head(4)

# Frequency
recent_months_2012 = month_2012_df.sort_values(by="mnth", ascending=False).head(4)
recent_months_2012['mnth'] = recent_months_2012['mnth'].map({9: "Sept", 10: "Okt", 11: "Nov", 12: "Des"})

# Monetary
years_rental = day_df.groupby('yr')['cnt'].sum().reset_index()
years_rental['yr'] = years_rental['yr'].map({0: '2011', 1: '2012'})


st.subheader("Recent Performance Rental Bikes Based on RFM Parameters")

col1, spacer, col2, spacer, col3 = st.columns([1, 0.2, 1, 0.2, 1])

with col1:
    avg_recency = round(recent_days_2012.cnt.mean())
    st.metric("Average (in recent Day)", value=avg_recency)

with col2:
    avg_frequency = round(recent_months_2012.cnt.mean())
    st.metric("Average (in recent Month)", value=avg_frequency)

with col3:
    avg_monetary = round(years_rental.cnt.mean()) 
    st.metric("Average (in Year)", value=avg_monetary)


# Data Visualisasi
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors_recency = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_Frequency = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_Monetary = ["#D3D3D3", "#72BCD4"]

# Recency
sns.barplot(y="cnt", x="dteday", data=recent_days_2012.sort_values(by="dteday", ascending=True), palette=colors_recency, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=30)
ax[0].tick_params(axis ='x', rotation=45, labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)

# Frequency
sns.barplot(y="cnt", x="mnth", data=recent_months_2012.sort_values(by="mnth", ascending=False), palette=colors_Frequency, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency (months)", loc="center", fontsize=30)
ax[1].tick_params(axis='x', labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)

# Monetary
sns.barplot(y="cnt", x="yr", data=years_rental.sort_values(by="yr", ascending=True), palette=colors_Monetary, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary (years)", loc="center", fontsize=30)
ax[2].tick_params(axis='x', labelsize=30)
ax[2].tick_params(axis='y', labelsize=30)

st.pyplot(fig)

st.empty() 

# Define by tahun 2011
year_2011_df = day_df[day_df['yr'] == 0]
# Define by bulan
month_2011_df = year_2011_df[['mnth', 'cnt']].groupby("mnth").sum().reset_index()


# Recency
recent_days_2011 = year_2011_df.sort_values(by="dteday", ascending=False)[["dteday", "cnt"]].head(4)

# Frequency
recent_months_2011 = month_2011_df.sort_values(by="mnth", ascending=False).head(4)
recent_months_2011['mnth'] = recent_months_2011['mnth'].map({9: "Sept", 10: "Okt", 11: "Nov", 12: "Des"})

# Monetary
years_rental = day_df.groupby('yr')['cnt'].sum().reset_index()
years_rental['yr'] = years_rental['yr'].map({0: '2011', 1: '2012'})


st.subheader("Last Year Performance Rental Bikes Based on RFM Parameters")

col1, spacer, col2, spacer, col3 = st.columns([1, 0.2, 1, 0.2, 1])

with col1:
    avg_recency = round(recent_days_2011.cnt.mean())
    st.metric("Average (in Day)", value=avg_recency)

with col2:
    avg_frequency = round(recent_months_2011.cnt.mean())
    st.metric("Average (in Month)", value=avg_frequency)

with col3:
    avg_monetary = round(years_rental.cnt.mean()) 
    st.metric("Average (in Year)", value=avg_monetary)


# Data Visualisasi
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors_recency = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]
colors_Frequency = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_Monetary = ["#D3D3D3", "#72BCD4"]

# Recency
sns.barplot(y="cnt", x="dteday", data=recent_days_2011.sort_values(by="dteday", ascending=True), palette=colors_recency, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=30)
ax[0].tick_params(axis ='x', rotation=45, labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)

# Frequency
sns.barplot(y="cnt", x="mnth", data=recent_months_2011.sort_values(by="mnth", ascending=False), palette=colors_Frequency, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency (months)", loc="center", fontsize=30)
ax[1].tick_params(axis='x', labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)

# Monetary
sns.barplot(y="cnt", x="yr", data=years_rental.sort_values(by="yr", ascending=True), palette=colors_Monetary, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary (years)", loc="center", fontsize=30)
ax[2].tick_params(axis='x', labelsize=30)
ax[2].tick_params(axis='y', labelsize=30)

st.pyplot(fig)

st.caption('Copyright (c) Muhammad Rian Tirta Nugraha')