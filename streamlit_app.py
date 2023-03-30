#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 19:26:51 2023
@author: danielspears
"""

import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from filter_func import filter_dataframe

Onet = {
11: 'Management Occupations',
13:	'Business and Financial Operations Occupations',
15:	'Computer and Mathematical Occupations',
17:	'Architecture and Engineering Occupations',
19: 'Life, Physical, and Social Science Occupations',
21: 'Community and Social Service Occupations', 
23: 'Legal Occupations',
25: 'Educational Instruction and Library Occupations',
27: 'Arts, Design, Entertainment, Sports, and Media Occupations',
29: 'Healthcare Practitioners and Technical Occupations',
31: 'Healthcare Support Occupations',
33: 'Protective Service Occupations',
35: 'Food Preparation and Serving Related Occupations',
37: 'Building and Grounds Cleaning and Maintenance Occupations',
39: 'Personal Care and Service Occupations',
41: 'Sales and Related Occupations',
43: 'Office and Administrative Support Occupations',
45: 'Farming, Fishing, and Forestry Occupations',
47: 'Construction and Extraction Occupations',
49: 'Installation, Maintenance, and Repair Occupations',
51: 'Production Occupations',
53: 'Transportation and Material Moving Occupations',
55: 'Military Specific Occupations'
}

pd.options.display.width = 180
pd.set_option('display.max_columns', None) 
today = dt.datetime.today().strftime('%m%d%Y')  

PROJ = "2031occproj.xlsx"

df = pd.read_excel(PROJ)
df = df[['Occupation', 'Occupation Code','Employment Percent Change, 2021-2031', 
         'Occupational Openings, 2021-2031 Annual Average', 'Median Annual Wage 2021',
         'Typical Entry-Level Education', 'Work Experience in a Related Occupation', 
         'Typical on-the-job Training', 'Less than high school diploma', 'High school diploma or equivalent', 
         'Some college, no degree', "Associate's degree", "Bachelor's degree", 
         "Master's degree", 'Doctoral or professional degree']]

# @st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)


df['Employment Percent Change, 2021-2031'] = df['Employment Percent Change, 2021-2031'].astype(float)

df['Onet'] = df['Occupation Code'].str[:2].astype(int)
df = df.replace({"Onet": Onet})
df = df.rename(columns={"Typical Entry-Level Education": "Typical_Entry_Level_Education", "Typical on-the-job Training": "Typical_on_the_job_Training", "Employment Percent Change, 2021-2031":"Employment_Percent_Change_2021_2031"})
dff = df.copy()
dfg = df.groupby("Onet")[["Employment_Percent_Change_2021_2031", "Median Annual Wage 2021", "Occupational Openings, 2021-2031 Annual Average"]].mean().reset_index()
dfb = df.groupby("Typical_Entry_Level_Education")[["Employment_Percent_Change_2021_2031", "Median Annual Wage 2021","Occupational Openings, 2021-2031 Annual Average"]].mean().reset_index()


# Sort the dataframe by "Employment_Percent_Change_2021_2031" column in descending order
dfb = dfb.sort_values(by="Employment_Percent_Change_2021_2031", ascending=False)

# print(dfb)


# Define a function for colouring  negative values red and positive values black
def highlight_max(val):
    if isinstance(val, (int, float)):
        color = 'green' if val >= 0 else 'red'
        return f'color: {color};'
    else:
        return ''
    

# ---- SIDEBAR ----
# st.sidebar.header("Filter table here:")
# educ = st.sidebar.multiselect(
#     "Education Level:",
#     options=df["Typical_Entry_Level_Education"].unique(),
#     default=df["Typical_Entry_Level_Education"].unique()
# )

# train= st.sidebar.multiselect(
#     "OJT:",
#     options=df["Typical_on_the_job_Training"].unique(),
#     default=df["Typical_on_the_job_Training"].unique(),
# )

# onet = st.sidebar.multiselect(
#     "ONET Job Family:",
#     options=df["Onet"].unique(),
#     default=df["Onet"].unique(),
# )

growth = st.sidebar.radio(
    "Select growth:",
    ("All", "Negative", "Positive")
)
if growth == "All":
    df = df.copy()
elif growth == "Negative":
    df = df.query("Employment_Percent_Change_2021_2031 < 0")
else:
    df = df.query("Employment_Percent_Change_2021_2031 >= 0")
    

# df = df.query("Typical_Entry_Level_Education == @educ & Typical_on_the_job_Training == @train & Onet ==@Onet")
# df = df.query("Typical_Entry_Level_Education == @educ & Onet == @onet")


# ---- MAINPAGE ----
st.title("2031 Occupational Projections")
st.markdown("##")
st.markdown("___")


df = filter_dataframe(df)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# Using apply method of style attribute of Pandas DataFrame
df = df.style.applymap(highlight_max, subset=['Employment_Percent_Change_2021_2031'])

st.markdown(hide_st_style, unsafe_allow_html=True)
st.dataframe(df.format(precision=2))# Same as st.write(df)

PROJ1 = "20202030Occupations_AllProjStatewide.xls"
dfstate = pd.read_excel(PROJ1, skiprows = 5 )
dfstate = dfstate[['Occ. \nCode ', 'Occupational Title ', '2030\nEmployment', 'Percent\nChange','Annual Total \nOpenings']]
dfstate =dfstate.rename(columns={"Occ. \nCode ": 'Occupation_Code',"Occupational Title ":"Occupation" , '2030\nEmployment' : "2031_Openings","Percent\nChange":"Employment_Percent_Change_2021_2031", "Annual Total \nOpenings":"Annual_Openings"})
# drop the first row
dfstate = dfstate.drop(0)
dfstate["Employment_Percent_Change_2021_2031"]= dfstate["Employment_Percent_Change_2021_2031"]*100
dfstate['Onet'] = dfstate['Occupation_Code'].str[:2].astype(int)
dfstate = dfstate.replace({"Onet": Onet})
# Calculate the sum of 2031_Openings for all occupations
total_openings = dfstate.loc[dfstate['Occupation'] == 'Total, All Occupations', '2031_Openings'].values[0]

# Calculate the percentage each occupation makes up of all jobs
dfstate['Percentage_of_All_Jobs'] = (dfstate['2031_Openings'] / total_openings) * 100

# print(dfstate)

PROJ2 = "20202030Occupations_AllProjRLMA7.xls"
df7 = pd.read_excel(PROJ2, skiprows = 5 )
df7 = df7[['Occ. \nCode ', 'Occupational Title ', '2030\nEmployment', 'Percent\nChange','Annual Total \nOpenings']]
df7 =df7.rename(columns={"Occ. \nCode ": 'Occupation_Code',"Occupational Title ":"Occupation", "2030\nEmployment" : "2031_Openings", "Percent\nChange":"Employment_Percent_Change_2021_2031", "Annual Total \nOpenings":"Annual_Openings"})
# drop the first row
df7 = df7.drop(0)
df7["Employment_Percent_Change_2021_2031"]= df7["Employment_Percent_Change_2021_2031"]*100
df7['Onet'] = df7['Occupation_Code'].str[:2].astype(int)
df7 = df7.replace({"Onet": Onet})
# Calculate the sum of 2031_Openings for all occupations
total_openings = df7.loc[df7['Occupation'] == 'Total, All Occupations', '2031_Openings'].values[0]

# Calculate the percentage each occupation makes up of all jobs
df7['Percentage_of_All_Jobs'] = (df7['2031_Openings'] / total_openings) * 100



PROJ3 = "uiratebyeducation.xlsx"
dfeduc = pd.read_excel(PROJ3)
dfeduc = dfeduc[['Month', 'Less than a high school diploma', 'High school graduates, no college', 'Some college or associate degree', "Bachelor's degree and higher"]]
dfeduc['Month'] = pd.to_datetime(dfeduc['Month'], format='%Y-%m')
dfeduc[["Less than a high school diploma","High school graduates, no college",
        "Some college or associate degree","Bachelor's degree and higher"]] = dfeduc[["Less than a high school diploma","High school graduates, no college", "Some college or associate degree","Bachelor's degree and higher"]].applymap(lambda x: x/1)

# Melt the education columns into a single column
dfeduc = dfeduc.melt(id_vars=['Month'], var_name='Education', value_name='Unemployment_Rate')
dfeduc = dfeduc.sort_values(by=['Education', 'Unemployment_Rate'], ascending=[True, False])
# Convert "Month" to a datetime column
dfeduc['Month'] = pd.to_datetime(dfeduc['Month'])

# Sort by "Month" column
dfeduc = dfeduc.sort_values('Month')

# Reset index
dfeduc = dfeduc.reset_index(drop=True)
print(dfeduc)



st.markdown("""---""") 

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='2031_projected_employment.csv',
    mime='text/csv',
)
st.markdown("""---""") 
st.caption("""
- Column sorting: sort columns by clicking on their headers.
- Column resizing: resize columns by dragging and dropping column header borders.
- Table resizing: resize tables by dragging and dropping the bottom right corner. Fullscreeen the app by clicking the double arrows in the top right of each chart.
- Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.
- Copy to clipboard: select one or multiple cells, copy them to the clipboard and paste them into your favorite spreadsheet software._
""")

