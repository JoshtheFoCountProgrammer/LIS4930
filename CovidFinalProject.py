import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Verify file path - update this if your CSV is in a different location
file_path = "covid_19_clean_complete.csv"  

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    print("Please verify the file path and try again.")
    exit()

# Convert Date to datetime format with error handling
try:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
except KeyError:
    print("Error: 'Date' column not found in the dataset.")
    print("Please verify the column names in the CSV file.")
    exit()

# Verify required columns exist
required_columns = ['Country/Region', 'Lat', 'Long', 'Confirmed', 'Deaths', 'Recovered']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Error: Missing columns in dataset: {', '.join(missing_columns)}")
    print("Please verify the CSV file structure.")
    exit()

# 1. Global Trend Visualization
plt.figure(figsize=(12, 6))
global_trend = df.groupby('Date').agg({
    'Confirmed': 'sum',
    'Deaths': 'sum',
    'Recovered': 'sum'
}).reset_index()

# Filter out invalid dates
global_trend = global_trend.dropna(subset=['Date'])

plt.plot(global_trend['Date'], global_trend['Confirmed'], label='Confirmed', marker='o')
plt.plot(global_trend['Date'], global_trend['Deaths'], label='Deaths', marker='s')
plt.plot(global_trend['Date'], global_trend['Recovered'], label='Recovered', marker='^')
plt.title('Global COVID-19 Trends (Jan 2020)')
plt.xlabel('Date')
plt.ylabel('Case Count')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('global_trend.png')
plt.show()

# 2. Country Comparison (Latest Date)
latest_date = df['Date'].max()
latest_data = df[df['Date'] == latest_date]

# Get top 10 countries by confirmed cases
top_countries = latest_data.groupby('Country/Region')['Confirmed'].sum() \
                          .nlargest(10).reset_index()

plt.figure(figsize=(12, 6))
# Changed palette to 'mako' (a valid seaborn palette)
sns.barplot(x='Confirmed', y='Country/Region', data=top_countries, palette='mako')
plt.title(f'Top 10 Countries by Confirmed Cases ({latest_date.strftime("%Y-%m-%d")})')
plt.xlabel('Confirmed Cases')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig('country_comparison.png')
plt.show()

# 3. Geographical Distribution Heatmap
plt.figure(figsize=(14, 8))
heatmap_data = df.groupby(['Country/Region', 'Lat', 'Long'])['Confirmed'] \
                .max().reset_index()

# Filter out invalid coordinates
heatmap_data = heatmap_data[(heatmap_data['Lat'] != 0) | (heatmap_data['Long'] != 0)]
heatmap_data = heatmap_data.dropna(subset=['Lat', 'Long'])

sns.scatterplot(
    x='Long',
    y='Lat',
    size='Confirmed',
    sizes=(20, 500),
    hue='Confirmed',
    palette='Reds',
    alpha=0.7,
    data=heatmap_data,
    legend=False
)

plt.title('Global Distribution of COVID-19 Cases (Heatmap)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.tight_layout()
plt.savefig('global_heatmap.png')
plt.show()

print("Visualizations created successfully!")
