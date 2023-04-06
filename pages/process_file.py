import pandas as pd
import datetime as dt
import math
import numpy as np
import streamlit as st
import plotly.express as px  # pip install plotly-express

pd.options.display.width = 180
pd.set_option("display.max_columns", None)
today = dt.datetime.today().strftime("%m%d%Y")

PROJ = "ExtJobOrderList.csv"

df = pd.read_csv(PROJ)

cities = ['Shreveport', 'Bossier', 'Bossier City', 'Benton', 'Haughton', 'Plain Dealing', 'Princeton', 'Mansfield', 'Stonewall', 'Keithville', 'Minden']

df = df[["JobTitle","Employer","Location","Salary","SalaryUnit","ONetCode","OccTitle","OccGroup","OccGroupTitle","NAICScode","NAICStitle","Source","PostDate","CloseDate",
    ]
]
df = df[df['Location'].isin(cities)]

print(df)