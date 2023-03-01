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
    CombinedAirQualityData = pd.read_csv("CombinedAirQualityData.csv")
    AirQualityDataHourly = pd.read_csv("AirQualityDataHourly.csv")

    Day = st.selectbox('Select Day', Date, help = 'Filter report to show only one day')
    Selected_Day = Week_data_95.loc[Week_data_95['Day'] == Day]
    Selected_Day_gov = AirQualityDataHourly.loc[AirQualityDataHourly['Day'] == Day]
    
    df = pd.merge(Selected_Day, Selected_Day_gov, how="left", on="Time")
    
    Feature = st.selectbox('Select Pollutant', Feature_List, help = 'Filter report to show only one pollutant')
    #Selected_Feature = df.loc[df[Feature] == Feature].any()

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
     F3 = 'PM2.5 particulate matter'
    elif (Feature == 'PM10 particulate matter'):
     F1 = '95-PM10(ug/m3)-slotA'
     F2 = '95-PM10(ug/m3)-slotB'
     F3 = 'PM10 particulate matter'  
         
    g0, g10= st.columns((100, 1))
    st.write("Hourly data for slot A and slot B with AURN data")
 
    fig = px.line(df, x = 'Time', y=[F1, F2, F3])
     
    g1, g2= st.columns((100, 1))
   
    g1.plotly_chart(fig, use_container_width=True)
    
    st.write("Weekly data for the average of slot A and slot B with AURN data") 
    
    g11, g21= st.columns((100, 1))
    
    CombinedAirQualityData['Difference'] = (CombinedAirQualityData[F3] - (0.5*(CombinedAirQualityData[F2] + CombinedAirQualityData[F1])))
    CombinedAirQualityData['Percentage'] = 100*(CombinedAirQualityData['Difference']) / (0.5*(CombinedAirQualityData[F1] + CombinedAirQualityData[F2]) + CombinedAirQualityData[F3])
    
    fig2 = px.bar(CombinedAirQualityData, x = 'Day', y='Difference')
     
    g11.plotly_chart(fig2, use_container_width=True)  
    
    g6, g8= st.columns((6, 1))
    
    #with g3:
    # st.dataframe(data=CombinedAirQualityData[F1], use_container_width=True)
    #with g4:
    # st.dataframe(data=CombinedAirQualityData[F2], use_container_width=True) 
    #with g5:
    # st.dataframe(data=CombinedAirQualityData[F3], use_container_width=True)  
     
    with g6:
     st.dataframe(data=CombinedAirQualityData[['Day', 'Time', 'Difference', 'Percentage']], use_container_width=True)  
    #with g7:
    # st.dataframe(data=CombinedAirQualityData[['Day', 'Time', 'Percentage']], use_container_width=True)
    
    with g8:
     st.write("Total difference") 
     st.write(sum(CombinedAirQualityData['Difference']))
     st.write("Average difference") 
     st.write(sum(CombinedAirQualityData['Difference'])/168)
     st.write("Percentage difference")
     st.write((sum(CombinedAirQualityData['Difference']) / sum(0.5*(CombinedAirQualityData[F1] + CombinedAirQualityData[F2]) + CombinedAirQualityData[F3]))*100)
     

    
    

 

