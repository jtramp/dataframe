import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from streamlit_app import dfstate, df7

# Create a merged dataframe with both dataframes
merged_df = pd.merge(dfstate, df7, on='Occupation', suffixes=('_state', '_7'))

# Create a new column to indicate which dataframe has the higher value
merged_df['Higher_Value'] = np.where(merged_df['Employment_Percent_Change_2021_2031_state'] > merged_df['Employment_Percent_Change_2021_2031_7'], 'State', '7')
merged_df = merged_df[['Occupation', '2031_Openings_state',  '2031_Openings_7','Annual_Openings_state', 'Annual_Openings_7','Employment_Percent_Change_2021_2031_state', 'Employment_Percent_Change_2021_2031_7','Percentage_of_All_Jobs_state','Percentage_of_All_Jobs_7','Onet_state','Higher_Value']]

def highlight_higher_value(s):
    if s['Higher_Value'] == 'State':
        if s['Employment_Percent_Change_2021_2031_7'] > s['Employment_Percent_Change_2021_2031_state']:
            return ['background-color: lightgreen; border: 1px white' if x == s['Employment_Percent_Change_2021_2031_7'] else '' for x in s]
        else:
            return ['background-color: lightgreen' if x == s['Employment_Percent_Change_2021_2031_state'] else '' for x in s]
    else:
        if s['Employment_Percent_Change_2021_2031_state'] > s['Employment_Percent_Change_2021_2031_7']:
            return ['background-color: lightgreen; border: 1px white' if x == s['Employment_Percent_Change_2021_2031_state'] else '' for x in s]
        else:
            return ['background-color: lightgreen' if x == s['Employment_Percent_Change_2021_2031_7'] else '' for x in s]

# print(merged_df)

# # # Apply the styling function to the Employment_Percent_Change_2021_2031 column
styled_df = merged_df.style.apply(highlight_higher_value, axis=1, subset=['Employment_Percent_Change_2021_2031_state', 'Employment_Percent_Change_2021_2031_7', 'Higher_Value'])


st.dataframe(styled_df.format(precision=2))

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