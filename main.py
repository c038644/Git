##########################################################
# to run: streamlit run main.py
##########################################################
from app import global_data, local
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

st.set_page_config(page_title='Credit Rating Calculator',  layout='wide', page_icon=':Calculator:')

#this is the header
 
t1, t2 = st.columns((0.07,1)) 

t2.title("Credit Rating Calculator")
t2.markdown("with Global and Local Customer Data")



with st.spinner('Updating Report...'):
    
    Customer_ID = pd.read_csv("files/Customer_ID.csv")
    Customer_ID = Customer_ID.drop(columns=['Unnamed: 0'])
    
    all_data = pd.read_csv("files/P7_test_df.csv")
    all_data = all_data.drop(columns=['Unnamed: 0'])

    Customer = st.selectbox('Select Customer', Customer_ID, help = 'Filter report to show only one customer')

    if Customer:
        Selected_Customer = all_data.loc[all_data['SK_ID_CURR'] == Customer]
        st.write(Selected_Customer)
        local(Selected_Customer)
        #local = requests.post("http://127.0.0.1:5000/local", Selected_Customer)
        #Selected_Customer.to_csv("files/selection.csv")
        #local = requests.get("https://c038644.herokuapp.com/local").json()
        #local_graph_df = pd.DataFrame.from_dict(local)
        #local_graph_df
   
   
    #local = requests.get("https://c038644.herokuapp.com/local").json()
    #local_graph_df = pd.DataFrame.from_dict(local)
    #local_graph_df
    
    g1, g2, g3 = st.columns((1,1,1))

    local_graph_df = pd.read_csv("files/Customer_score.csv")
    
    fig = px.bar(local_graph_df, x = 'Feature', y='Importance')
    
 
    fig.update_layout(title_text="Local Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g1.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = local_graph_df.iat[0,3],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Rating", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.26], 'color': 'red'},
                {'range': [0.26, 0.36], 'color': 'orange'},
                {'range': [0.36, 1], 'color': 'green'}],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': 0.31}}))

    fig2.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})

    g2.plotly_chart(fig2, use_container_width=True) 

    
    #global_graph_df = requests.get("http://127.0.0.1:5000/global_data").json()
    global_graph = requests.get("https://c038644.herokuapp.com/global_data").json()

    #global_graph.type()
    #st.json(global_graph_df)

    #global_graph_df = pd.DataFrame.from_dict('global_data', orient="index")
    #global_graph_df

    #global_graph_df = pd.read_csv("files/Global_Features.csv")

    #global_graph_df = global_graph_df.drop(columns=['Unnamed: 0'])
    
    #global_graph_df = pd.DataFrame([global_graph])
    #global_graph_df = pd.DataFrame({global_graph})
    
  
    #global_graph_df = pd.read_json(global_graph, orient='index')
    
    #global_graph_df = json.loads(global_graph)
    
    #global_graph
    
    global_graph_df = pd.DataFrame.from_dict(global_graph)
    
    #global_graph_df = pd.DataFrame(eval(global_graph))
    
    fig = px.bar(global_graph_df, x = 'Feature', y='Importance')
    
    fig.update_layout(title_text="Global Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g3.plotly_chart(fig, use_container_width=True)

    Selected_Customer = pd.read_csv("files/selection.csv")

    Feature_List = pd.read_csv("files/P7_Features.csv")

    Feature = st.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')

    Selected_Feature = all_data.loc[all_data[Feature] == Feature].any()

    g4, g5 = st.columns((1,2))

    fig = px.scatter(Selected_Customer, x = 'SK_ID_CURR', y = Feature)
    
    fig.update_layout(title_text="Local Feature Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g4.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(all_data, x = 'SK_ID_CURR', y = Feature)
    
    fig.update_layout(title_text="Global Feature Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g5.plotly_chart(fig, use_container_width=True)
