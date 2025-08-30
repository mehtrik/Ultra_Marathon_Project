# Ultra_Marathon_Project

## Project Overview

This project performs an exploratory data analysis (EDA) of ultramarathon races to uncover trends, patterns, and insights about race results, participants, and performance metrics. Using Python, we explore a variety of aspects including participant demographics, race distances, completion times, and performance distributions.

The goal of this project is to provide insights that could help runners, coaches, and race organizers better understand ultramarathon performance and participation trends.

## Dataset

### Source: Local CSV file (ultramarathon_data.csv)

### Size: Too large to include directly on GitHub

### Columns (examples):

* Runner_Name — Name of the participant

* Age — Age of the runner

* Gender — Gender of the runner

* Race_Name — Name of the ultramarathon

* Distance_km — Race distance in kilometers

* Finish_Time — Total finish time

* Year — Year of the race

## Cleaning and sorting data

Before performing analysis, the dataset was cleaned and organized to ensure consistency and usability. Key steps included:

### 1. Extracting Country to filter the data based on this identifier and cleaning event names in order to filter for this as well

'''python
# Add a Country column by extracting text inside parentheses
df['Country'] = df['Event name'].str.extract(r'\((.*?)\)')
print(df[['Event name', 'Country']].head())  # sanity check

# Remove the country part from Event name (anything inside parentheses)
df['Event name'] = df['Event name'].str.replace(r"\s*\(.*?\)", "", regex=True)
'''
