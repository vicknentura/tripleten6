Title: Triple Ten Data Analysis (Python Script)

Description:

This Python script analyzes data provided by Triple Ten, likely related to taxi trips. It performs the following tasks:

Data Loading: Reads CSV files containing trip information (df_trips), Ohare loop data (df_ohare_loop), and dropoff data (df_dropoff).
Quality Assurance (QA):
Checks each DataFrame for the number of rows and columns (check_values function).
Counts zeros, null/NaN values, and inf/-inf values.
Data Cleaning:
Drops rows from df_dropoff containing zeros to avoid processing issues.
Splits the 'start_ts' column in df_dropoff into separate 'date' and 'time' columns.
Converts the 'start_ts' column in df_dropoff to datetime format and extracts the day.
Converts the 'date' column in df_dropoff to datetime format.
Assumes df_trips has a 'company_name' column and removes unwanted characters using regular expressions.
Data Visualization (Bokeh):
Creates a scatter plot showing weather condition vs. trip duration with quantile ranges (using factor_cmap for color mapping).
Generates an informative HTML snippet using Bokeh's Div class.
Creates a scatter plot with markers representing weather conditions, duration (seconds) on the x-axis, and start time on the y-axis (using factor_mark for markers and factor_cmap for color mapping).
Requirements:

Python 3.x
pandas
requests
BeautifulSoup
Bokeh
scipy
numpy
matplotlib
seaborn
tabulate
Instructions:

Install the required libraries using pip install pandas requests beautifulsoup4 bokeh scipy numpy matplotlib seaborn tabulate.
Place the script and the CSV files (moved_project_sql_result_01.csv, moved_project_sql_result_04.csv, moved_project_sql_result_07.csv) in the same directory.
Run the script from the command line using python script_name.py.
Notes:

This script assumes specific column names and data formats. You may need to modify it based on your actual data.
Consider adding comments within the code to improve readability and maintainability.
Additional Information:

The script utilizes Bokeh for interactive visualizations. Refer to the Bokeh documentation (https://bokeh.org/) for more details.
