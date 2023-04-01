import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express
from streamlit_app import dfg

st.title("2031 Occupations Scatterplot")
st.subheader('Hover on chart and click the double arrows to Fullscreen')
# st.markdown("##")
fig = px.scatter(
    dfg,
    x="Median Annual Wage 2021",
    text='Onet',
    y="Employment_Percent_Change_2021_2031",
    size="Occupational Openings, 2021-2031 Annual Average",
    color="Onet",
    opacity = .7,
    labels={'Median Annual Wage 2021': 'Median Wage', 'Employment_Percent_Change_2021_2031':'% Change'},
    hover_data=['Onet']
)
fig.update_traces(textposition='top center')
fig.update_layout(width=800, height=600)

# Show the chart
# fig.show()
st.plotly_chart(fig)

st.caption("""
- Column sorting: sort columns by clicking on their headers.
- Column resizing: resize columns by dragging and dropping column header borders.
- Table resizing: resize tables by dragging and dropping the bottom right corner.  Fullscreeen the app by clicking the double arrows in the top right of the chart.
- Search: search through data by clicking a table, using hotkeys (⌘ Cmd + F or Ctrl + F) to bring up the search bar, and using the search bar to filter data.
- Copy to clipboard: select one or multiple cells, copy them to the clipboard and paste them into your favorite spreadsheet software._
""")