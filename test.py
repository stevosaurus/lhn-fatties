import numpy as np
import pandas as pd
import random
import plotly.express as px
from datetime import datetime

rows_to_keep = 43

sheet_data = pd.read_excel("https://docs.google.com/spreadsheets/d/1DuYUj2ODS8D3PWK42ZopUD1dqcg89ckI6vPn71LidGo/export?format=xlsx")
sheet_data = sheet_data.iloc[:rows_to_keep].drop(columns=["Overall % Lost", "Imgur"]).dropna(axis=1, how="all")
sheet_data = sheet_data.rename(columns={"$": "Pot Contribution", "Starting 1/1/22": "Starting Weight"})
sheet_data = sheet_data.melt(id_vars=["Participant", "Pot Contribution", "Paid?", "Starting Weight"], var_name="Date", value_name="Weight")
sheet_data["Starting Weight"] = pd.to_numeric(sheet_data["Starting Weight"])
sheet_data["Weight"] = pd.to_numeric(sheet_data["Weight"])
sheet_data = sheet_data.dropna(subset=["Weight", "Starting Weight"]).sort_values(by=["Participant", "Date"]).reset_index()

by_participant = sheet_data.groupby("Participant")

sheet_data["Previous Week Weight"] = by_participant["Weight"].shift(1)
sheet_data.loc[sheet_data["Previous Week Weight"].isnull(), "Previous Week Weight"] = sheet_data.loc[sheet_data["Previous Week Weight"].isnull(), "Starting Weight"]
sheet_data["Weight Difference"] = sheet_data["Weight"] - sheet_data["Previous Week Weight"]

sheet_data["Cumulative Weight Lost"] = by_participant["Weight Difference"].transform(pd.Series.cumsum)
sheet_data["Participant Index"] = by_participant.ngroup()

participant_colors = ["#%06x" % random.randint(0, 0xFFFFFF) for participant, _ in by_participant]

fig = px.line(sheet_data, x="Date", y="Weight", color='Participant')
fig.update_yaxes(range=[130, 400])

display(fig)