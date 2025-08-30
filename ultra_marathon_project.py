#%%
#import libraries
import pandas as pd
import seaborn as sns

#path to csv file
file_path = r"C:\Users\nicky\OneDrive\Documents\Python Projects\TWO_CENTURIES_OF_UM_RACES.csv"
#read data set csv file
df = pd.read_csv(file_path)
#%%

#print the first 5 rows and check shape
print(df.head())
print(df.shape)

#%%
#check data types
print(df.dtypes)
#%%

#%%
# Add a Country column by extracting text inside parentheses
df['Country'] = df['Event name'].str.extract(r'\((.*?)\)')
print(df[['Event name', 'Country']].head())  # sanity check
# %%

# Exploratory analysis: 50km/50mi races in 2020
df1 = df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020)]
print(df1.shape)

#%%
# Results from the Everglades 50 Mile Ultra Run (USA)
df2 = df[df['Event name'] == 'Everglades 50 Mile Ultra Run (USA)']
print(df2.head())

#%%
# Combine above filters with Country column
df3 = df[(df['Event distance/length'].isin(['50km','50mi'])) &
         (df['Year of event'] == 2020) &
         (df['Country'] == 'USA')]
print(df3.shape)
print(df3.head())
# %%

#%%
# Remove the country part from Event name (anything inside parentheses)
df3['Event name'] = df['Event name'].str.replace(r"\s*\(.*?\)", "", regex=True)

print(df3[['Event name', 'Country']].head(10))
# %%

#%%
#clean up athlete age
df3.loc[:, 'Athlete_age'] = 2020 - df3['Athlete year of birth']

print(df3['Athlete_age'].head())
# %%

#%%
#remove the 'h' (hour) from athlete performace
df3['Athlete performance'] = df3['Athlete performance'].str.replace("h", "", regex=False).str.strip()

print(df3['Athlete performance'].head())
# %%

#%%
#drop columns: Athlete Club, Athlete Country, Athlete year of birth, Athlete Age Category
df3 = df3.drop(['Athlete club', 'Athlete country', 'Athlete year of birth', 'Athlete age category'], axis = 1 )

print(df3.head())
# %%

#%%
#drop mistakenly created cloumn 'athelte age' and rename 'athlete age' -> 'Athlete age'
df3 = df3.drop(columns=['athelte_age'])
#%%
df3 = df3.rename(columns={'athlete_age': 'Athlete age'})
# %%

#%%
#clean up null vaues
print(df3.isna().sum())
df3 = df3.dropna()
#%%

#%%
#check for duplicate values
df3[df3.duplicated() == True]
# %%

#%%
#reset index
df3.reset_index(drop = True)
# %%

#%%
#fix types
df3['Athlete age'] = df3['Athlete age'].astype(int)
df3['Athlete average speed'] = df3['Athlete average speed'].astype(float)
# %%

#%%
#rename columns to make it easy to query in analysis
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
# %%

#%%
#reorder columns
df4 = df3[['race_day', 
           'race_name', 
           'race_length', 
           'race_number_of_finishers', 
           'athlete_id', 
           'athlete_gender', 
           'athlete_age', 
           'athlete_performance', 
           'athlete_average_speed']]
# %%

#%%
#chart analysis examples
#number of races 50mi vs 50km for males and females
sns.histplot(df4, x = 'race_length', hue = 'athlete_gender')
# %%

#%%
#average speed distribution for 50mile race for males and females
sns.displot(
    data=df4[df4['race_length'] == '50mi'],
    x='athlete_average_speed',
    hue='athlete_gender',
    kind='hist',
)
# %%

#%%
#Evaluate the distribution of the age of runners by their speed for males and females
sns.lmplot(
    data=df4,
    x='athlete_age',
    y='athlete_average_speed',
    hue='athlete_gender'
)
# %%

##Exploratory questions to anlayse for this data

#Q.1 What is the difference in speed for the 50k,50mi male to female
#%%
print(
    df4.groupby(['race_length', 'athlete_gender'])['athlete_average_speed'].mean()
)
# %%

#Q.2 What age groups are the best in the 50mi race (athlete has ran 20+ races minimum)
print(
    df3.query('race_length == "50mi"')
    .groupby('athlete_age')['athlete_average_speed']
    .agg(['mean','count'])
    .query('count>19')
    .sort_values('mean',ascending=False)
)
# %%
