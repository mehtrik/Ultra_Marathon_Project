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

* Extracting Country and Cleaning Event Names

```python
# Add a Country column by extracting text inside parentheses
df['Country'] = df['Event name'].str.extract(r'\((.*?)\)')
print(df[['Event name', 'Country']].head())

# Remove the country part from Event name (anything inside parentheses)
df['Event name'] = df['Event name'].str.replace(r"\s*\(.*?\)", "", regex=True)
```
* Filtering for specfic races
```python
# 50km/50mi races in 2020
df1 = df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020)]
print(df1.shape)

# Results from the Everglades 50 Mile Ultra Run (USA)
df2 = df[df['Event name'] == 'Everglades 50 Mile Ultra Run (USA)']
print(df2.head())

# Combine above filters with Country column
df3 = df[(df['Event distance/length'].isin(['50km','50mi'])) &
         (df['Year of event'] == 2020) &
         (df['Country'] == 'USA')]
print(df3.shape)
print(df3.head())
```
* Cleaning Athlete Age
```python
# Calculate athlete age from year of birth
df3.loc[:, 'Athlete_age'] = 2020 - df3['Athlete year of birth']
print(df3['Athlete_age'].head())
```
* Removing the 'h' in athlete performace in order for this to be a number value
```python
# Remove 'h' (hours) and strip whitespace
df3['Athlete performance'] = df3['Athlete performance'].str.replace("h", "", regex=False).str.strip()
print(df3['Athlete performance'].head())
```
* Dropping unnecessary columns
```python
df3 = df3.drop(['Athlete club',
                'Athlete country',
                'Athlete year of birth',
                'Athlete age category'],
                axis=1)
print(df3.head())
```
* handling duplicate columns, null values and fixing data types
```python
# Drop mistakenly created column and rename
df3 = df3.drop(columns=['athelte_age'])
df3 = df3.rename(columns={'athlete_age': 'Athlete age'})

# Drop null values
print(df3.isna().sum())
df3 = df3.dropna()

# Check for duplicates
df3[df3.duplicated() == True]

# Reset index
df3 = df3.reset_index(drop=True)

#fixing data types
df3['Athlete age'] = df3['Athlete age'].astype(int)
df3['Athlete average speed'] = df3['Athlete average speed'].astype(float)
```
* Renaming and reording columns
```python
# Rename for easier analysis
df3 = df3.rename(columns = {'Year of event':'year',
                            'Event dates': 'race_day',
                            'Event name' : 'race_name',
                            'Event distance/length' : 'race_length',
                            'Event number of finishers' : 'race_number_of_finishers',
                            'Athlete performance' : 'athlete_performance',
                            'Athlete gender' : 'athlete_gender',
                            'Athlete average speed' : 'athlete_average_speed',
                            'Athlete ID' : 'athlete_id',
                            'Athlete age' : 'athlete_age'})

# Reorder columns
df4 = df3[['race_day', 
           'race_name', 
           'race_length', 
           'race_number_of_finishers', 
           'athlete_id', 
           'athlete_gender', 
           'athlete_age', 
           'athlete_performance', 
           'athlete_average_speed']]
```
### Example snippet of the cleaned dataset after processing:

| race\_day  | race\_name               | race\_length | race\_number\_of\_finishers | athlete\_id | athlete\_gender | athlete\_age | athlete\_performance | athlete\_average\_speed |
| ---------- | ------------------------ | ------------ | --------------------------- | ----------- | --------------- | ------------ | -------------------- | ----------------------- |
| 2020-01-25 | Everglades 50 Mile Ultra | 50 mi        | 120                         | 1001        | M               | 34           | 6:15                 | 8.0                     |
| 2020-01-25 | Everglades 50 Mile Ultra | 50 mi        | 120                         | 1002        | F               | 29           | 7:10                 | 7.0                     |

### This cleaned and sorted dataset is now ready for exploratory analysis and visualisation

# Exploratory Analysis & Charts

### After cleaning and sorting the dataset, several visualizations were created to explore patterns in ultramarathon performance:

* Number of races in the 50mi vs 50km for males and females
```python
#number of races 50mi vs 50km for males and females
sns.histplot(df4, x='race_length', hue='athlete_gender', multiple='stack')
```
<img width="589" height="433" alt="image" src="https://github.com/user-attachments/assets/250c6dbe-6379-40cc-b022-e87098196523" />

* Average speed distrivution for 50mi race for males and females
```python
sns.displot(
    data=df4[df4['race_length'] == '50mi'],
    x='athlete_average_speed',
    hue='athlete_gender',
    multiple='stack',
    kind='hist',
)
```
<img width="614" height="489" alt="image" src="https://github.com/user-attachments/assets/9542d9a8-2d16-4390-8c42-e33fa714e53e" />

* Evaluate the distribution of the age of runners by their speed for males and females

  ```python
  sns.lmplot(
    data=df4,
    x='athlete_age',
    y='athlete_average_speed',
    hue='athlete_gender',
    palette={'M':'blue','F':'orange'},
    height=6,
    aspect=1.2
  )

<img width="824" height="589" alt="image" src="https://github.com/user-attachments/assets/bfce558b-beb3-4ea0-a62b-9164e50e3b8b" />

## Exploratory Questions

### After cleaning and visualizing the data, we can explore specific questions to better understand ultramarathon performance patterns.

### Q1: Difference in Speed Between Males and Females for 50 km and 50 mi Races
We can compare the average speef of male and female athletes for each race distance:
```python
# Calculate mean speed by race length and gender
print(
    df4.groupby(['race_length', 'athlete_gender'])['athlete_average_speed'].mean()
)
```
Results shown below:

| Race Length | Athlete Gender | Average Speed (km/h) |
| ----------- | -------------- | -------------------- |
| 50 km       | F              | 7.08                 |
| 50 km       | M              | 7.74                 |
| 50 mi       | F              | 6.83                 |
| 50 mi       | M              | 7.26                 |


### Q2: Best Age Groups in 50-Mile Races (Athletes with 20+ Races)
To identify the most competitive age groups among highly experienced runners:
```python
print(
    df3.query('race_length == "50mi"')
       .groupby('athlete_age')['athlete_average_speed']
       .agg(['mean','count'])
       .query('count > 19')
       .sort_values('mean', ascending=False)
        .head(5)
)
```
Results shown below:

 | Athlete Age | Average Speed (km/h) | Number of Races |
| ----------- | -------------------- | --------------- |
| 29          | 7.90                 | 135             |
| 23          | 7.78                 | 55              |
| 28          | 7.58                 | 107             |
| 30          | 7.57                 | 157             |
| 25          | 7.54                 | 91              |
