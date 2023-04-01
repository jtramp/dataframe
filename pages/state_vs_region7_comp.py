import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from streamlit_app import dfstate, df7
from filter_func import filter_dataframe2


st.subheader('State vs. 7th RMLA - Growth Comparisons')
# Create a merged dataframe with both dataframes
merged_df = pd.merge(dfstate, df7, on='Occupation', suffixes=('_state', '_7'))

# Create a new column to indicate which dataframe has the higher value
merged_df['Higher_Value'] = np.where(merged_df['Employment_Percent_Change_2021_2031_state'] > merged_df['Employment_Percent_Change_2021_2031_7'], 'State', '7')
merged_df = merged_df[['Occupation', '2031_Openings_state',  '2031_Openings_7','Annual_Openings_state', 'Annual_Openings_7','Employment_Percent_Change_2021_2031_state', 'Employment_Percent_Change_2021_2031_7','Percentage_of_All_Jobs_state','Percentage_of_All_Jobs_7','Onet_state','Higher_Value']]
column_mapping = {
    'Occupation': 'Occ',
    '2031_Openings_state': '2031_State_Openings',
    '2031_Openings_7': '2031_7th_Openings',
    'Annual_Openings_state': 'State_Openings',
    'Annual_Openings_7': '7th_Openings',
    'Employment_Percent_Change_2021_2031_state': '%_State_Change',
    'Employment_Percent_Change_2021_2031_7': '%_7th_Change',
    'Percentage_of_All_Jobs_state': '%_of_all_State_jobs',
    'Percentage_of_All_Jobs_7': '%_of_all_7th_jobs',
    'Onet_state': 'Onet',
    'Higher_Value': 'Higher_Value'
}

merged_df = merged_df.rename(columns=column_mapping)
# print(merged_df)

merged_df = filter_dataframe2(merged_df)
def highlight_higher_value(s):
    if s['Higher_Value'] == 'State':
        if s['%_7th_Change'] > s['%_State_Change']:
            return ['background-color: lightgreen; border: 1px white' if x == s['%_7th_Change'] else '' for x in s]
        else:
            return ['background-color: lightgreen' if x == s['%_State_Change'] else '' for x in s]
    else:
        if s['%_State_Change'] > s['%_7th_Change']:
            return ['background-color: lightgreen; border: 1px white' if x == s['%_State_Change'] else '' for x in s]
        else:
            return ['background-color: lightgreen' if x == s['%_7th_Change'] else '' for x in s]

# print(merged_df)

# # # Apply the styling function to the Employment_Percent_Change_2021_2031 column
styled_df = merged_df.style.apply(highlight_higher_value, axis=1, subset=['%_State_Change', '%_7th_Change', 'Higher_Value'])
# styled_df = styled_df[['Occ', '2031_State_Openings',  '2031_7th_Openings','State_Openings', '7th_Openings','%_State_Change', '%_7th_Change','%_of_all_State_jobs','%_of_all_7th_jobs','Onet']]
st.dataframe(styled_df.format(precision=0))
# st.dataframe(styled_df)
st.caption("""
- Column sorting: sort columns by clicking on their headers.
- Column resizing: resize columns by dragging and dropping column header borders.
- Table resizing: resize tables by dragging and dropping the bottom right corner.  Fullscreeen the app by clicking the double arrows in the top right of the chart.
- Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.
- Copy to clipboard: select one or multiple cells, copy them to the clipboard and paste them into your favorite spreadsheet software._
""")
# # # styled dataframe to HTML
# html = styled_df.to_html()

# # # Display the HTML in Streamlit
# st.write(html, unsafe_allow_html=True)