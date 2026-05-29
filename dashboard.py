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
    compare_mode = st.checkbox("Compare Two States")
    st.header('Filter')
    if compare_mode:
        state1 = st.selectbox('State 1', options=list(data['state'].unique()), index=0, key="state1")
        state2 = st.selectbox('State 2', options=list(data['state'].unique()), index=1, key="state2")
    else:
        state=st.selectbox('State', options=["All States"] + list(data['state'].unique()), index=0)
    commodity=st.selectbox('Commodity', options=["Show All Commodities"] + list(data['commodity'].unique()), index=0)
    price=st.selectbox(
    "Price Type",
    ["min_x0020_price",
     "max_x0020_price",
     "modal_x0020_price"]
)
st.markdown("""
<style>

/* Metric Cards */
[data-testid="stMetric"]{
    background: rgba(255,255,255,0.03);
    padding: 15px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827,
        #0f172a
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Main headings */
h1, h2, h3 {
    color: #5ffae5 !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #5ffae5 !important;
}

/* Metric value */
[data-testid="stMetricValue"] {
    color: #5ffae5 !important;
}

/* Metric label */
[data-testid="stMetricLabel"] {
    color: #A8D8FF !important;
}
[data-testid="stMetric"] {
    background: #1c2740;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid rgba(95,250,229,0.15);
    box-shadow: 0 0 12px rgba(95,250,229,0.08);
}

""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

    st.caption(
        "Source: AGMARKNET, Ministry of Agriculture & Farmers Welfare, Govt. of India"
    )

df = data.copy() #df is the dataframe that we will filter and show in the dashboard
if compare_mode:
    df_compare = df[
        df["state"].isin([state1, state2])
    ]

    if commodity != "Show All Commodities":
        df_compare = df_compare[
            df_compare["commodity"] == commodity
        ]
else:
    if state != "All States":
        df = df[
            df['state'] == state
        ]
    if commodity != "Show All Commodities":
        df = df[
            df['commodity'] == commodity
        ]
#Various metrics to show in the dashboard
total_records = len(df)
unique_states = df['state'].nunique()
unique_commodities = df['commodity'].nunique()
avg_price = df["modal_x0020_price"].mean()
avg_price = round(avg_price)

# Display metrics in columns
col1,col2,col3,col4 =st.columns([1,1,1,1.2])

with col1:
    ###with st.container(border=True):
        st.metric("Total Records", total_records)
        st.markdown("aross all markets")
with col2:
    ###with st.container(border=True):
        st.metric("Unique States", unique_states)
        st.markdown("+4UT's")
with col3:
    ###with st.container(border=True):
        st.metric("Unique Commodities", unique_commodities)
        st.markdown("unique items")
with col4:
    ###with st.container(border=True):
        st.metric("Average  Modal Price", f"₹ {avg_price}")
        st.markdown("per quintal")

# Grouping data for visuals/charts
grouped_1=df.groupby("commodity")["modal_x0020_price"].mean().sort_values(ascending=False).head(10)
grouped_2=df.groupby("state")["modal_x0020_price"].mean().sort_values(ascending=False).head(6)
df["price_spread"] = df["max_x0020_price"] - df["min_x0020_price"]
grouped_3 = df.groupby("commodity")["price_spread"].mean().sort_values(ascending=False).head(10)


if compare_mode:
    
    col_1 = st.columns(1)[0]

    with col_1:
        with st.container(border=True):

            if commodity == "Show All Commodities":

                st.warning(
                    "Please select a commodity to compare between states."
                )

            else:

                df_compare = df[
                    (df["state"].isin([state1, state2])) &
                    (df["commodity"] == commodity)
                ]

                comparison = (
                    df_compare
                    .groupby("state")[price]
                    .mean()
                    .reindex([state1, state2])
                    .reset_index()
                )

                missing_states = comparison[
                    comparison[price].isna()
                ]["state"].tolist()

                if missing_states:
                    st.warning(
                        f"No data available for {', '.join(missing_states)} "
                        f"for {commodity}."
                    )

                # Create plotting copy
                plot_df = comparison.copy()

                plot_df["label"] = plot_df[price].apply(
                    lambda x: "No Data" if pd.isna(x) else f"₹{x:.0f}"
                )

                plot_df[price] = plot_df[price].fillna(0)

                fig1 = px.bar(
                    plot_df,
                    x="state",
                    y=price,
                    color="state",
                    title=f"{commodity}: {state1} vs {state2}",
                    labels={
                        "state": "State",
                        price: price.replace("_x0020_", " ").title()
                    },
                    text="label"
                )
                fig1.update_traces(
    marker=dict(cornerradius=5)
)
                fig1.update_layout(
                    margin=dict(l=20, r=20, t=60, b=20),
                    font=dict(size=12),
                    showlegend=False
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True,
                    theme="streamlit"
                )

else:

    col_1, col_2 = st.columns(2)
    with col_1:
        with st.container(border=True):
            fig1 = px.bar(
            grouped_1,
            y=grouped_1.index,
            x=grouped_1.values,
            labels={"y": "Commodities", "x": "Average Modal Price"},
            orientation='h',
            title="Top 10 Commodities",
            color=grouped_1.values,
            color_continuous_scale=[
    "#5FFAE5",
    "#36D399",
    "#10B981",
    "#047857"
]
            )
            fig1.update_traces(
    marker=dict(cornerradius=5)
)
            fig1.update_layout(
                yaxis=dict(autorange="reversed")
            )
            fig1.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(size=12)
    )
            st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

    with col_2:
        with st.container(border=True):
            fig2 = px.bar(grouped_2, y=grouped_2.index, x=grouped_2.values, labels={"y": "State", "x": "Average Modal Price"}, title="Top 6 States by Average Modal Price", orientation='h')
            fig2.update_layout(
                yaxis=dict(autorange="reversed")
            )
            fig2.update_traces(
    marker=dict(cornerradius=5)
)
            fig2.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(size=12)
    )
            st.plotly_chart(fig2, use_container_width=True, theme="streamlit")

if commodity=="Show All Commodities": 
    with st.container(border=True):
        # Prepare pie chart (donut) with improved styling
        pie_names = grouped_3.index
        pie_values = grouped_3.values
        top_name = grouped_3.idxmax() if len(grouped_3) > 0 else None
        pull = [0.08 if name == top_name else 0 for name in pie_names]

        fig3 = px.pie(
            names=pie_names,
            values=pie_values,
            title="Top 10 Commodities by Average Price Spread (₹)",
            hole=0.4,
            color=pie_names,
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

        fig3.update_traces(
            textposition='inside',
            textinfo='percent+label',
            pull=pull,
            hovertemplate='%{label}: ₹%{value:.2f}<br>%{percent}',
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )

        fig3.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(size=12),
            legend_title_text='Commodity'
        )

        st.plotly_chart(fig3, use_container_width=True, theme="streamlit")
else:
    st.info("Select 'Show All Commodities' to view commodity spread distribution.")

#Download button 
left,right = st.columns([3.8,1])
with right:
    csv=df.to_csv(index=False)
    st.download_button(
    label="Download CSV",
    data=csv,
    file_name="agri_market_prices.csv",
    mime="text/csv",
    key="download-csv",
    icon_position="right"
    )
    
# SHOW DATA
with st.container(border=True):

    st.subheader("Market Data")

    st.dataframe(df,use_container_width=True)