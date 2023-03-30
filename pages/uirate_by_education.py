import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from streamlit_app import dfeduc


fig = px.area(dfeduc, x="Month", y="Unemployment_Rate", color="Education",
              labels={"Month": "Years", "Unemployment_Rate": "Unemployment Rate", "Education": "Education Level"},
              title="Unemployment Rate by Education Level over Time",
              hover_data={"Month": "|%B %Y"})

fig.update_layout(
    xaxis_tickformat="%b %Y",
    hovermode="x"
)
colors = ['rgb(255, 215, 0)', 'rgb(255, 177, 78)', 'rgb(0, 0, 255)','rgb(220, 105, 86)']

for i, color in enumerate(colors):
    fig['data'][i]['line']['color'] = color


for trace in fig.data:
    trace.stackgroup = trace.name

st.plotly_chart(fig, use_container_width=True)
st.caption("""
- Column sorting: sort columns by clicking on their headers.
- Column resizing: resize columns by dragging and dropping column header borders.
- Table resizing: resize tables by dragging and dropping the bottom right corner. Fullscreeen the app by clicking the double arrows in the top right of each chart.
- Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.
- Copy to clipboard: select one or multiple cells, copy them to the clipboard and paste them into your favorite spreadsheet software._
""")