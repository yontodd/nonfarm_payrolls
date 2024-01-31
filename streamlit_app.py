# Data libraries
import pandas_datareader as pdr
import datetime
import time
from datetime import date
import pandas as pd

# Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Set the start and end dates for your data
# End date set for today, so will pull all data up to latest releases

start_date = datetime.datetime(1960, 1, 1)
end_date = date.today()

# Define the FRED indicator codes you want to fetch.
establishment_survey= ['PAYEMS',"USPRIV",'UNRATE',"CES0500000003","AWHAETP"]

# Fetch the data from FRED
establishment_survey_data = pdr.get_data_fred(establishment_survey, start_date, end_date)
establishment_survey_data.columns = ["Headline payrolls","Private payrolls","Unemployment rate","Average hourly earnings","Average Weekly Hours"]
establishment_survey_data["Headline payrolls"] = establishment_survey_data["Headline payrolls"].diff()
establishment_survey_data["Private payrolls"] = establishment_survey_data["Private payrolls"].diff()
establishment_survey_data["Average hourly earnings (w/w)"] = round(establishment_survey_data["Average hourly earnings"].pct_change() * 100,2)
establishment_survey_data["Average hourly earnings (y/y)"] = round(establishment_survey_data["Average hourly earnings"].pct_change(12) * 100, 2)

household_survey = ["CE16OV","CIVPART","LNS12300060"]

household_survey_data = pdr.get_data_fred(household_survey,start_date,end_date)
household_survey_data.columns = ["Employment level change (m/m)","Labor force participation rate","Prime-age employment to population ratio"]
household_survey_data["Employment level change (m/m)"] = household_survey_data["Employment level change (m/m)"].diff()