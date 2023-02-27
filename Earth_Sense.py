import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
#import requests
#import json
#import matplotlib.pyplot as plt

#def graph(Day):
    



    #ax = Day[["95-NO2(ug/m3)-slotA","95-NO2(ug/m3)-slotB","Nitrogen dioxide", "Time"]].plot(kind="line", x="Time", figsize=(19,5), title="Wednesday NO2 Levels")
    #ax.legend(["95-NO2(ug/m3)-slotA", "95-NO2(ug/m3)-slotB","Nitrogen dioxide"])
    #for p in ax.patches:
    #    ax.annotate( str( round(p.get_height(),3) ), (p.get_x() * 1.005, p.get_height() * 1.005))

    #ax.title.set_size(20)
    #plt.box(False)

st.set_page_config(page_title='Credit Rating Calculator',  layout='wide', page_icon=':Calculator:')

#this is the header
 
t1, t2 = st.columns((0.07,1)) 

t2.title("Credit Rating Calculator")
t2.markdown("with Global and Local Customer Data")


with st.spinner('Updating Report...'):
    
    Date = pd.read_csv("Day.csv")
    Week_data_95 = pd.read_csv("Week_data_95.csv")
    #Customer_ID = Customer_ID.drop(columns=['Unnamed: 0'])
    
    Wednesday_gov = pd.read_csv("Wednesday_gov.csv")
    #
    # all_data = all_data.drop(columns=['Unnamed: 0'])

    Day = st.selectbox('Select Customer', Date, help = 'Filter report to show only one customer')


    #if Day:
    #    Selected_Day = Week_data_95.loc[Week_data_95['Day'] == Day]
    #    st.write(Day)
        #Selected_Customer.to_csv("files/selection.csv")
        #local = requests.get("local").json()
        #st.json(local) 
    
    #graph(Day)

    df = pd.merge(Week_data_95, Wednesday_gov, how="left", on="Time")
    
    graph_df = df[['Time', 'Ozone']]

    g1, g2= st.columns((10, 1))

    #local_graph_df = pd.read_csv("files/Customer_score.csv")
    
    #fig = px.line(graph_df, x = 'Time', y='Ozone')
    df = px.data.gapminder().query("Day==Date")
    
    fig = px.line(df, x = 'Time', y='Ozone', title='Life expectancy in Canada')
    #fig.update_layout(title_text="Local Features Graph",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g1.plotly_chart(fig, use_container_width=True)

