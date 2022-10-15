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
import pickle
#from sklearn.model_selection import train_test_split
#from imblearn.under_sampling import RandomUnderSampler
#from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title='Credit Rating Calculator',  layout='wide', page_icon=':Calculator:')

#this is the header
 
t1, t2 = st.columns((0.07,1)) 

t2.title("Credit Rating Calculator")
t2.markdown("with Global and Local Customer Data")

def local(Selected_Customer, test_df):

  #Local Features Case for a chosen Selected Customer

  feature_list = list(test_df.columns)

  X = test_df.drop(['TARGET'], axis=1).values
  y = test_df['TARGET'].values

  data = Selected_Customer.drop(['TARGET'], axis=1).values

  filename = 'files/final_model.sav'
  loaded_model = pickle.load(open(filename, 'rb'))
  score = loaded_model.fit(X, y).predict(data)
    
  #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
  #undersample = RandomUnderSampler(sampling_strategy=1)
  #X_train, y_train = undersample.fit_resample(X_train, y_train)
  #rfc = RandomForestClassifier(max_depth=13, min_samples_leaf=2, min_samples_split=8, n_estimators=552)
  #score = rfc.fit(X_train, y_train).predict(data)

  Credit_given_test = np.max(loaded_model.predict_proba(data))

  if score==0:
    credit_score=Credit_given_test

  else:
    credit_score=(1-Credit_given_test)

  print('Get importances')

  # Get numerical feature importances
  importances = list(loaded_model.feature_importances_)

  # List of tuples with variable and importance
  feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

  # Sort the feature importances by most important first
  feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

  #Ten most important features
  ten_most_important = feature_importances[0:10]

  ten_most_important_df = pd.DataFrame(ten_most_important)

  ten_most_important_df.columns = ['Feature', 'Importance']

  ten_most_important_df['Credit Score'] = credit_score

  ten_most_important_df['Credit Granted?'] = None

  if credit_score>=0.35:
    ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('Yes')
  elif credit_score>=0.25:
    ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('Risky')
  else:
    ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('No')

  return(ten_most_important_df)

with st.spinner('Updating Report...'):
    
    #Customer_ID = pd.read_csv("files/Customer_ID.csv")
    #Customer_ID = Customer_ID.drop(columns=['Unnamed: 0'])
    
    all_data = pd.read_csv("files/P7_test_df.csv")
    all_data = all_data.drop(columns=['Unnamed: 0'])

    Customer_ID = requests.get("https://c038644.herokuapp.com/labels").json()
    Customer = st.selectbox('Select Customer', Customer_ID, help = 'Filter report to show only one customer')
    
    Customer_df = pd.DataFrame.from_dict(Customer)
    #if Customer:
    #Selected_Customer = all_data.loc[all_data['SK_ID_CURR'] == Customer]
    #st.write(Selected_Customer)
    data = pd.read_json(
    requests.get("https://c038644.herokuapp.com/customer", params={"selector": Customer_df}).json()
    )
    data
        #local_graph_df = local(Selected_Customer, all_data)
   
    #local = requests.get("https://c038644.herokuapp.com/local").json()
    #local_graph_df = pd.DataFrame.from_dict(local)
    
    g1, g2, g3 = st.columns((1,1,1))

    fig = px.bar(local_graph_df, x = 'Feature', y='Importance')
  
    fig.update_layout(title_text="Local Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g1.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = local_graph_df.iat[0,2],
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

    global_graph = requests.get("https://c038644.herokuapp.com/global_data").json()

    global_graph_df = pd.DataFrame.from_dict(global_graph)
    
    fig = px.bar(global_graph_df, x = 'Feature', y='Importance')
    
    fig.update_layout(title_text="Global Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g3.plotly_chart(fig, use_container_width=True)

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
