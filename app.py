import requests
from bs4 import BeautifulSoup
import pandas as pd
import bokeh
import scipy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tabulate


#Set up individual data frames based on data provided by Triple Ten
df_trips = pd.read_csv('moved_project_sql_result_01.csv')
df_ohare_loop = pd.read_csv('moved_project_sql_result_04.csv')
df_dropoff = pd.read_csv('moved_project_sql_result_07.csv')


#Quality assurance (QA) check to identify any irregularities in the datasets

def check_values(df):
    print(f"Checking {df.shape[0]} rows and {df.shape[1]} columns in DataFrame...")
    
    # count zeros
    zero_count = (df == 0).sum().sum()
    print(f"Zeros found: {zero_count}")
    
    # count null/nan and inf/-inf
    df_inf = df.replace([np.inf, -np.inf], np.nan)
    nan_count = df_inf.isnull().sum().sum()
    print(f"Null/NaN values found: {nan_count}")

check_values(df_trips)
check_values(df_dropoff)
check_values(df_ohare_loop)


#Drop rows where zeros were found to avoid any downstream processing issues
df_dropoff = df_dropoff[(df_dropoff != 0).all(axis=1)]


# Split the 'start_ts' column into 'date' and 'time' columns
df_dropoff[['date', 'time']] = df_dropoff['start_ts'].str.split(' ', expand=True)

# Now you have your DataFrame with separate 'date' and 'time' columns
print(df_dropoff.info())



# Convert the 'start_ts' column to datetime format
df_dropoff['start_ts'] = pd.to_datetime(df_dropoff['start_ts'])

# Extract the day from the 'start_ts' column
df_dropoff['day'] = df_dropoff['start_ts'].dt.day

print(df_dropoff.info())


# Convert the 'date' column to datetime format
df_dropoff['date'] = pd.to_datetime(df_dropoff['date'])

df_dropoff.dtypes


# assume df_trips is your dataframe and 'company_name' is the column with the unwanted characters

df_trips['company_name'] = df_trips['company_name'].str.replace(r'\d{4} - \d{5}', '', regex=True)



# Assuming df_ohare_loop is your DataFrame
df_ohare_loop = df_ohare_loop.sort_values(by='number_of_trips', ascending=False)

# Now df_ohare_loop is sorted by the 'average_trips' column in descending order
print("The most popular destinations of taxi rides in Chicago in November 2017 were:")
display(df_ohare_loop.head(10))



from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, jitter

# Assuming your dataframe is named df_dropoff

classes = list(sorted(df_dropoff["weather_conditions"].unique()))

p = figure(height=400, x_range=classes, background_fill_color="#efefef",
           title="Weather Condition vs Trip Duration with quantile ranges")
p.xgrid.grid_line_color = None

g = df_dropoff.groupby("weather_conditions")
upper = g.duration_seconds.quantile(0.80)
lower = g.duration_seconds.quantile(0.20)
source = ColumnDataSource(data=dict(base=classes, upper=upper, lower=lower))

error = Whisker(base="base", upper="upper", lower="lower", source=source,
                level="annotation", line_width=2)
error.upper_head.size=20
error.lower_head.size=20
p.add_layout(error)

p.scatter(jitter("weather_conditions", 0.3, range=p.x_range), "duration_seconds", source=df_dropoff,
          alpha=0.5, size=13, line_color="white",
          color=factor_cmap("weather_conditions", "Light7", classes))

show(p)



# Compagnies de taxi visualisation deux (Bokeh scatter with markers = ['weather_conditions'], x = ['duration_seconds'], y = ['time'])
#https://docs.bokeh.org/en/latest/docs/examples/basic/data/transform_markers.html

from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, factor_mark

# Create legend groups, markers, and color mapping based on unique weather conditions
SPECIES = df_dropoff['weather_conditions'].unique()  # Get unique weather conditions
MARKERS = ['hex', 'circle_x'] * (len(SPECIES) // 2 + 1)  # Assign markers cyclically

# Use your data source (assuming it's a pandas DataFrame)
source = df_dropoff

p = figure(title="Weather Conditions", background_fill_color="#fafafa")
p.xaxis.axis_label = 'Duration (seconds)'
p.yaxis.axis_label = 'Start Time'

p.scatter(x="duration_seconds", y="time", source=source,
          legend_group="weather_conditions", fill_alpha=0.4, size=12,
          marker=factor_mark('weather_conditions', MARKERS, SPECIES),
          color=factor_cmap('weather_conditions', 'Category10_3', SPECIES))

p.legend.location = "top_left"
p.legend.title = "Weather Conditions"

show(p)