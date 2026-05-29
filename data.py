import streamlit as st
import pandas as pd
import plotly.express as px

#cache the data loading function to improve performance
@st.cache_data
def load_data(nrows):
    data = pd.read_csv("agri_market_prices.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data["arrival_date"] = pd.to_datetime(data["arrival_date"],format="mixed")
    return data

data=load_data(10000)
# Set page configuration
st.title('Agricultural Market Prices')
st.markdown('This dashboard shows the agricultural market prices over time.')
#Sidebar for filters
with st.sidebar:
    st.header('Filter')
    state=st.selectbox('State', options=["All States"] + list(data['state'].unique()), index=0)
    commodity=st.selectbox('Commodity', options=["Show All Commodities"] + list(data['commodity'].unique()), index=0)
    price=st.selectbox(
    "Price Type",
    ["min_x0020_price",
     "max_x0020_price",
     "modal_x0020_price"]
)
st.sidebar.markdown("Source: AGMARKNET, Ministry of Agriculture & Farmers Welfare, Govt. of India")

df = data.copy() #df is the dataframe that we will filter and show in the dashboard

if state != "All States":
    df = df[df['state'] == state]

if commodity != "Show All Commodities":
    df = df[df['commodity'] == commodity]
#Various metrics to show in the dashboard
total_records = len(df)
unique_states = df['state'].nunique()
unique_commodities = df['commodity'].nunique()
avg_price = df["modal_x0020_price"].mean()
avg_price = round(avg_price)

# Display metrics in columns
col1,col2,col3,col4 =st.columns([1,1,1,1.2])
with col1:
    with st.container(border=True):
        st.metric("Total Records", total_records)
        st.markdown("aross all markets")
with col2:
    with st.container(border=True):
        st.metric("Unique States", unique_states)
        st.markdown("+4UT's")
with col3:
    with st.container(border=True):
        st.metric("Unique Commodities", unique_commodities)
        st.markdown("unique items")
with col4:
    with st.container(border=True):
        st.metric("Average  Modal Price", f"₹ {avg_price}")
        st.markdown("per quintal")

# Grouping data for visuals/charts
grouped_1=df.groupby("commodity")["modal_x0020_price"].mean().sort_values(ascending=False).head(10)
grouped_2=df.groupby("state")["modal_x0020_price"].mean().sort_values(ascending=False).head(6)
df["price_spread"] = df["max_x0020_price"] - df["min_x0020_price"]
grouped_3 = df.groupby("commodity")["price_spread"].mean().sort_values(ascending=False).head(10)

col_1, col_2, col_3 = st.columns([1,1,0.7])
with col_1:
    fig1 = px.bar(grouped_1, y=grouped_1.index, x=grouped_1.values, labels={"y": "Commodity", "x": "Average Modal Price"}, title="Top 10 Commodities by Average Modal Price")
    st.plotly_chart(fig1)

with col_2:
    fig2 = px.bar(grouped_2, y=grouped_2.index, x=grouped_2.values, labels={"y": "State", "x": "Average Modal Price"}, title="Top 6 States by Average Modal Price")
    st.plotly_chart(fig2)

with col_3:
    fig3 = px.bar(grouped_3, y=grouped_3.index, x=grouped_3.values, labels={"y": "Commodity", "x": "Average Price Spread"}, title="Top 10 Commodities by Average Price Spread")
    st.plotly_chart(fig3)

#Download button 
left,right = st.columns([3.8,1])
with right:
    csv=df.to_csv(index=False)
    st.download_button(csv, "agri_market_prices.csv", "Download CSV")
    
# SHOW DATA
st.dataframe(df)
