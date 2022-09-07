from msilib.schema import Feature
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests


st.set_page_config(page_title='Credit Rating Calculator',  layout='wide', page_icon=':Calculator:')

#this is the header
 

t1, t2 = st.columns((0.07,1)) 

t2.title("Credit Rating Calculator")
t2.markdown("with Global and Local Customer Data")

## Data

with st.spinner('Updating Report...'):
    
    Customer_ID = pd.read_csv("https://github.com/c038644/Git/files/Customer_ID.csv")
    Customer_ID = Customer_ID.drop(columns=['Unnamed: 0'])
    
    all_data = pd.read_csv("https://github.com/c038644/Git/files/P7_test_df.csv")
    all_data = all_data.drop(columns=['Unnamed: 0'])

    Customer = st.selectbox('Select Customer', Customer_ID, help = 'Filter report to show only one customer')

    if Customer:
        Selected_Customer = all_data.loc[all_data['SK_ID_CURR'] == Customer]
        st.write(Selected_Customer)
        Selected_Customer.to_csv("https://github.com/c038644/Git/files/selection.csv")
        local = requests.get("http://localhost:5000/local").json()
       

    g1, g2, g3 = st.columns((1,1,1))

    local_graph_df = pd.read_csv("https://github.com/c038644/Git/files/Customer_score.csv")
    
    fig = px.bar(local_graph_df, x = 'Feature', y='Importance')
    
 
    fig.update_layout(title_text="Local Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g1.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = local_graph_df.iat[0,3],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Rating", 'font': {'size': 24}},
        #delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.27], 'color': 'red'},
                {'range': [0.27, 0.37], 'color': 'orange'},
                {'range': [0.37, 1], 'color': 'green'}],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': 0.32}}))

    fig2.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})

    g2.plotly_chart(fig2, use_container_width=True) 

    global_data = requests.get("http://localhost:5000/global_data").json()

    global_graph_df = pd.read_csv("https://github.com/c038644/Git/files/Global_Features.csv")
    
    fig = px.bar(global_graph_df, x = 'Feature', y='Importance')
    
    fig.update_layout(title_text="Global Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g3.plotly_chart(fig, use_container_width=True)

    Selected_Customer = pd.read_csv("https://github.com/c038644/Git/files/selection.csv")

    Feature_List = pd.read_csv("https://github.com/c038644/Git/files/P7_Features.csv")

    Feature = st.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')

    Selected_Feature = all_data.loc[all_data[Feature] == Feature].any()

    g4, g5 = st.columns((1,2))

    fig = px.scatter(Selected_Customer, x = 'SK_ID_CURR', y = Feature)
    
    fig.update_layout(title_text="Local Feature Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g4.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(all_data, x = 'SK_ID_CURR', y = Feature)
    
    fig.update_layout(title_text="Global Feature Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g5.plotly_chart(fig, use_container_width=True)
