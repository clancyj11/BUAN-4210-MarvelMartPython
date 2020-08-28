'''
Python Project - Marvel Mart Project

Joey Clancy
March 13, 2020
'''

#Importing necessary libraries here...
import pandas as pd;
import numpy as np;
# Using nltk only to build frequency distribution (See ORDER PRIORITY section)
import nltk;

pd.set_option('display.float_format', lambda x: '%.2f' % x)

# PART 1: DATA PREPROCESSING
'''
For summary of each part, see documentation.
'''

df = pd.read_csv(r"Marvel_Mart_Sales_Project_Master.csv")

# Check for ALL MISSING DATA in each individual column
sumNA = df.isna().sum()

# Find all incorrect data in the COUNTRY column
# Create empty list to store indexes of float values
indexCountry = []
for index, row in df.iterrows():
# Converts valid values to floats, and pulls the index of the corresponding values
    try:
        row['Country'] = float(row['Country'])
        if type(row['Country']) == float:
            indexCountry.append(index)
    except:
        1==1
# Because we know the indexes of the bad data, we can use .replace()
for index in indexCountry:
    df.replace(df['Country'][index], 'NULL', inplace = True)

# Replace all missing values in ITEM TYPE with "NULL"
df["Item Type"] = df["Item Type"].fillna("NULL")

# Find all incorrect data in the ORDER ID column
# Use the same method of cleaning as done in COUNTRY
invalidID = []
for index, row in df.iterrows():
   if row['Order ID'].isalpha():
       invalidID.append(index)
for index in invalidID:
    df.replace(df['Order ID'][index], 'NULL', inplace = True)
'''
# Search for invalid or missing priority codes with a frequency distribution
freqDist = nltk.FreqDist(df['Order Priority'])
freqDist.plot(10)
'''
# Replace all "nan" values in ORDER PRIORITY with "NULL"
df["Order Priority"] = df["Order Priority"].fillna("NULL")

# Export to new csv file
df.to_csv("Marvel_Mart_Sales_clean.csv", sep = ',', index = False)

# Verification of cleansed data
'''
print(df['Country'].unique())
print(df['Item Type'].unique())
print(df['Order Priority'].unique())
'''
sumNaFinal = df.isna().sum()

# PART 2: GENERAL STATISTICS

# Create a dictionary with headers as keys, and column data as the values
# NOT NEEDED TILL PART C
mainDict = df.to_dict('list')

# 1
# A
# Returns the top ten countries according to the amount of orders that were placed
initialSalesCount = df['Country'].value_counts()
countrySales = pd.DataFrame(initialSalesCount).reset_index()
countrySales.columns = ['Country', 'Total Sales']

# B
# Returns the sales channel and how many orders took place via each channel
initialChannelCount = df['Sales Channel'].value_counts()
salesChannelCount = pd.DataFrame(initialChannelCount).reset_index()
salesChannelCount.columns = ['Channel Type', 'Count']

# C
# SEE DOCUMENTATION
years = []
for i in mainDict['Order Date']:
    years.append(i[-4:])
profits = []
for i in mainDict['Total Profit']:
    profits.append(i)
yearlyProfits = pd.DataFrame(list(zip(years, profits)))
yearlyProfits.columns = ['Year', 'Profit']
yearlyProfits = yearlyProfits.groupby(['Year']).agg('sum')
yearlyProfits = yearlyProfits.sort_values(by=['Profit'], ascending = False)
yearlyProfits = yearlyProfits.reset_index()

# Section is to append all required stats from above to text file
# Create new text file in write mode
file = open("Marvel_Mart_Rankings.txt", 'w+')

# Append Section A
file.write('COUNTRIES WITH MOST ORDERS: \n')
for row in range(0, 10):
    file.write("%s: %d\n" % (countrySales['Country'][row], countrySales['Total Sales'][row]))
# Answer the question of where new shipping center should be located and why
file.write("Shipping Center Location: Cape Verde\n"
           "Reasoning: Cape Verde is the country that has the most orders without a shipping center.\n")

# Append Section B
file.write("\nORDER CHANNEL FREQUENCIES:\n")
for row in range(0, 2):
    file.write("%s: %d\n" % (salesChannelCount['Channel Type'][row], salesChannelCount['Count'][row]))
# Answer the question regarding the most frequent order channel
file.write("Most frequent order channel: %s\n" % (salesChannelCount['Channel Type'][0]))

# Append Section C
file.write("\nTOP 3 YEARS IN PROFIT: \n")
for row in range(0,3):
    file.write("%s: %d\n" % (yearlyProfits['Year'][row], yearlyProfits['Profit'][row]))
# Answering which year had the highest profit
file.write("We had the highest profits in %s." % (yearlyProfits['Year'][0]))

# Close the file
file.close()

# 2
# A
# Empty list, sums of all required columns will be appended below
sumList = []
sumList.append(df['Units Sold'].sum())
sumList.append(df['Unit Cost'].sum())
sumList.append(df['Total Revenue'].sum())
sumList.append(df['Total Cost'].sum())
sumList.append(df['Total Profit'].sum())
# Creates a data frame including indexes, and totals from sumList
sums = pd.DataFrame(sumList, index=['Total Units Sold', 'Total Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']).reset_index()
sums.columns = ['Category', 'Total']

# B
# Empty list, sums of all required columns will be appended below
meanList = []
meanList.append(df['Units Sold'].mean())
meanList.append(df['Unit Cost'].mean())
meanList.append(df['Total Revenue'].mean())
meanList.append(df['Total Cost'].mean())
meanList.append(df['Total Profit'].mean())
# Creates a data frame including indexes, and averages from meanList
means = pd.DataFrame(meanList, index=['Average Units Sold', 'Average Unit Cost', 'Average Revenue', 'Average Cost', 'Average Profit']).reset_index()
means.columns = ['Category', 'Averages']

# C
# Empty list, sums of all required columns will be appended below
maxList = []
maxList.append(df['Units Sold'].max())
maxList.append(df['Unit Cost'].max())
maxList.append(df['Total Revenue'].max())
maxList.append(df['Total Cost'].max())
maxList.append(df['Total Profit'].max())
# Creates a data frame including indexes, and maximums from maxList
maximums = pd.DataFrame(maxList, index=['Max Units Sold', 'Max Unit Cost', 'Max Revenue', 'Max Cost', 'Max Profit']).reset_index()
maximums.columns = ['Category', 'Maximums']

# Section is to append all required stats from above to another text file
file2 = open('Marvel_Mart_Calc.txt', 'w+')

# Append Section A
file2.write('TOTALS: \n')
for row in range(0, 5):
    file2.write("%s: %d\n" % (sums['Category'][row], sums['Total'][row]))

# Append Section B
file2.write('\nAVERAGES: \n')
for row in range(0, 5):
    file2.write("%s: %d\n" % (means['Category'][row], means['Averages'][row]))

# Append Section C
file2.write('\nMAXIMUMS: \n')
for row in range(0, 5):
    file2.write("%s: %d\n" % (maximums['Category'][row], maximums['Maximums'][row]))

# Close the file
file2.close()

# PART 3 CROSS-REFERENCE STATISTICS

#SEE DOCUMENTATION
# Create dataframe from region and country columns
regionDF = df[['Region', 'Country']].copy()
# Drop the duplicates from our new data frame
regionDF = regionDF.drop_duplicates()
# Use group by to merge the country rows by region, and join with a comma
regionDF = regionDF['Country'].groupby([regionDF.Region]).apply(list).reset_index()
# Convert the two series that make up regionDF data frame into lists
countryList = regionDF['Country'].tolist()
regionList = regionDF['Region'].tolist()
# Because the two lists are now the same length, we can zip them into a dictionary
# The tolist() function above, split the one large string into one string per country
regionDict = dict(zip(regionList, countryList))
# Convert the dictionary to a dataframe with index orient and transpose
finalRegionDF = pd.DataFrame.from_dict(regionDict, orient='index').transpose()
# FINALLY! EXPORT TO CSV!
finalRegionDF.to_csv('Countries_By_Region.csv', index = False)
# EXCELSIOR!!!
# 153 lines of code w/o comments