import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from streamlit_app import dfb

# Assume df contains the data

fig2 = px.scatter_3d(dfb, x='Typical_Entry_Level_Education', y='Median Annual Wage 2021',z= 'Employment_Percent_Change_2021_2031',
              color="Typical_Entry_Level_Education")
fig2.update_layout(width=1000, height=800,  
                   scene_camera=dict(eye=dict(x=-0.8, y=-1.8, z=0.6)),
                   plot_bgcolor='rgb(240, 240, 240)',
                   paper_bgcolor='rgb(240, 240, 240)',
                   scene=dict(
                        xaxis_title='Education',
                        yaxis_title='Wage',
                        zaxis_title='% Change 2021-2031'))
st.plotly_chart(fig2)

st.caption("""
- Column sorting: sort columns by clicking on their headers.
- Column resizing: resize columns by dragging and dropping column header borders.
- Table resizing: resize tables by dragging and dropping the bottom right corner. Fullscreeen the app by clicking the double arrows in the top right of the chart.
- Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.
- Copy to clipboard: select one or multiple cells, copy them to the clipboard and paste them into your favorite spreadsheet software._
""")