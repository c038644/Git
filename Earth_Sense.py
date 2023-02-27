import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Air Quality Analysis',  layout='wide', page_icon=':Calculator:')

#this is the header
 
t1, t2 = st.columns((0.07,1)) 

t2.title("Air Quality Analysis")
t2.markdown("with Zephyr and AURN Data")


with st.spinner('Updating Report...'):
    
    Date = pd.read_csv("Day.csv")
    Week_data_95 = pd.read_csv("Week_data_95.csv")
    Feature_List = pd.read_csv("Feature_List.csv")
    
    AirQualityDataHourly = pd.read_csv("AirQualityDataHourly.csv")

    Day = st.selectbox('Select Customer', Date, help = 'Filter report to show only one customer')
    Selected_Day = Week_data_95.loc[Week_data_95['Day'] == Day]
    Selected_Day_gov = AirQualityDataHourly.loc[AirQualityDataHourly['Day'] == Day]
    
    df = pd.merge(Selected_Day, Selected_Day_gov, how="left", on="Time")
    
    Feature = st.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')
    Selected_Feature = df.loc[df[Feature] == Feature].any()

    g1, g2= st.columns((10, 1))
    
    #fig = px.line(df, x = 'Time', y=Feature)
    fig = px.line(df, x = 'Time', y=['95-NO2(ug/m3)-slotA', '95-NO2(ug/m3)-slotB'])
     
    g1.plotly_chart(fig, use_container_width=True)
 

