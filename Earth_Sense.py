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

    Day = st.selectbox('Select Day', Date, help = 'Filter report to show only one day')
    Selected_Day = Week_data_95.loc[Week_data_95['Day'] == Day]
    Selected_Day_gov = AirQualityDataHourly.loc[AirQualityDataHourly['Day'] == Day]
    
    df = pd.merge(Selected_Day, Selected_Day_gov, how="left", on="Time")
    
    Feature = st.selectbox('Select Pollutant', Feature_List, help = 'Filter report to show only one pollutant')
    #Selected_Feature = df.loc[df[Feature] == Feature].any()

    g1, g2= st.columns((100, 1))

    
    if (Feature == 'Nitric oxide'):
     F1 = '95-NO(ug/m3)-slotA'
     F2 = '95-NO(ug/m3)-slotB'
     F3 = 'Nitric oxide'
    elif (Feature == 'Nitrogen dioxide'):
     F1 = '95-NO2(ug/m3)-slotA'
     F2 = '95-NO2(ug/m3)-slotB'
     F3 = 'Nitrogen dioxide'
    elif (Feature == 'Ozone'):
     F1 = '95-O3(ug/m3)-slotA'
     F2 = '95-O3(ug/m3)-slotB'
     F3 = 'Ozone' 
    elif (Feature == 'PM2.5 particulate matter'):
     F1 = '95-PM2.5(ug/m3)-slotA'
     F2 = '95-PM2.5(ug/m3)-slotB'
     F3 = 'PM2.5 particulate matter (Hourly measured)'
    elif (Feature == 'PM10 particulate matter'):
     F1 = '95-PM10(ug/m3)-slotA'
     F2 = '95-PM10(ug/m3)-slotB'
     F3 = 'PM10 particulate matter (Hourly measured)'  

 
    fig = px.line(df, x = 'Time', y=[F1, F2, F3])
     
    g1.plotly_chart(fig, use_container_width=True)

    g3, g4= st.columns((100, 1))
    
    #df['Difference'] = ((df[F3] - ((df[F2] + df[F1])/2))/(df[F3] + df[F2] + df[F1])) * 100
    df['Difference'] = (df[F3] - (df[F2] + df[F1])/2)
    
    fig2 = px.line(df, x = 'Time', y='Difference')
     
    g3.plotly_chart(fig2, use_container_width=True)
 

