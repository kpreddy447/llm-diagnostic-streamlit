import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the CSV file
file_path = "bing_maps_telemetry_50000.csv"  
df = pd.read_csv(file_path)

# Basic info
print("Shape of data:", df.shape)
# print("\nData types:\n", df.dtypes)
# print("\nFirst 5 rows:\n", df.head())
# print("\nMissing values:\n", df.isnull().sum())
print("\nSummary statistics:\n", df.describe(include='all'))
