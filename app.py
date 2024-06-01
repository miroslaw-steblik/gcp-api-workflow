import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery
import plotly.graph_objects as go


#------------------------- Configuration --------------------------------------#
st.set_page_config(
    page_title="Fantasy Football League App",
    layout="wide",
    initial_sidebar_state="expanded",
    )

# st.html("styles.html")

#------------------------- Load Data ------------------------------------------#
#### BigQuery connection
credentials = service_account.Credentials.from_service_account_info(
     st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials)

# BigQuery SQL query

@st.cache_data()
def get_data():
    # use backticks for table name
    query = """
        SELECT * FROM `streamlit-apps-424120.league.fantasy_league_teams`

    """
    return client.query(query).to_dataframe()

df = get_data()

#------------------------- Sidebar -------------------------------------------#
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "About"]
)



#------------------------- Dashboard Page ------------------------------------#
if page == "Dashboard":
    st.title("Dashboard")


    tiles_upper = st.columns([1,1,1,1])
    tiles_upper[0].metric(label="Total Teams", value=df.shape[0])

    max_strength = df['strength_overall_home'].max()
    min_strength = df['strength_overall_home'].min()
    avg_strength = df['strength_overall_home'].mean()


    tiles_upper[1].metric(label="Max Strength", value=max_strength)
    tiles_upper[2].metric(label="Min Strength", value=min_strength)
    tiles_upper[3].metric(label="Avg Strength", value=avg_strength)

    #team with max strength
    max_strength_team = df[df['strength_overall_home'] == max_strength]
    st.write(f"Team with Max Strength: {max_strength_team['name'].values[0]}")

    #team with min strength
    min_strength_team = df[df['strength_overall_home'] == min_strength]
    st.write(f"Team with Min Strength: {min_strength_team['name'].values[0]}")


    # Create a plot
    fig = px.bar(df, x='name', y='strength', title='Team Strength')
    st.plotly_chart(fig)


    # Create a bar chart with Plotly Express
    multi_bar_chart = px.bar(df, x='name', y=['strength_overall_home', 'strength_overall_away'], title='Team Strength')
    # Convert the Plotly Express figure to a Plotly Graph Objects figure
    multi_bar_chart = go.Figure(multi_bar_chart)
    # Modify the layout to create a grouped bar chart
    multi_bar_chart.update_layout(barmode='group')
    # Display the chart
    st.plotly_chart(multi_bar_chart)

    # Create a table
    st.write("Data Table")
    st.write(df)





#------------------------- About Page ----------------------------------------#
if page == "About":
    st.title("About Page")
    st.write("This app is created by Streamlit and Google Cloud Platform")


#------------------------- Footer --------------------------------------------#
st.markdown(
    """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

#------------------------- End of App -----------------------------------------#
