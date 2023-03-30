import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from filter_func import filter_dataframe
from streamlit_app import dfb
st.title("Education")
st.markdown("##")
fig1 = px.bar(dfb, x="Typical_Entry_Level_Education", y="Employment_Percent_Change_2021_2031",
             color="Typical_Entry_Level_Education",
             labels={
                 "Typical_Entry_Level_Education": "Education Level",
                 "Employment_Percent_Change_2021_2031": "Employment % Change"
             },
             text = "Median Annual Wage 2021",
             hover_data=["Median Annual Wage 2021", "Occupational Openings, 2021-2031 Annual Average"]
            )

fig1.update_layout(
    title="Employment % Change by Education Level",
    xaxis_title="Education Level",
    yaxis_title="Employment % Change",
    width=800,
    height=800
)
fig1.update_traces(texttemplate='%{y}%<br>Wage: $%{text:.2s}', textposition='outside')

# fig1.show()

st.plotly_chart(fig1)
st.caption("""
- Column sorting: sort columns by clicking on their headers.
- Column resizing: resize columns by dragging and dropping column header borders.
- Table resizing: resize tables by dragging and dropping the bottom right corner.  Fullscreeen the app by clicking the double arrows in the top right of the chart.
- Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.
- Copy to clipboard: select one or multiple cells, copy them to the clipboard and paste them into your favorite spreadsheet software._
""")