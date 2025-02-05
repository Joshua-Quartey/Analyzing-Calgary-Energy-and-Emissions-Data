# Analyzing-Calgary-Energy-and-Emissions-Data

### Introduction
This project is an exploratory data analysis of the benchmarkYYC dataset provided by the city of Calgary. 
Benchmark YYC is a voluntary energy benchmarking program for eligible buildings runby the City of Calgary in the province of Alberta.

###  Methodology
The purpose of this project is to perform an in-depth analysis of the City of Calgary’s Building Energy Benchmarking dataset. 

The project uses Python, Regular Expressions (Regex), Pandas (for minimal tabular operations), NumPy, and Matplotlib to preprocess, analyze, and visualize the 
data. 

The project is carried in stages including cleaning the dataset, extracting relevant data using Regex, 
performing aggregations, detecting outliers, and conducting exploratory visualizations.

#### Data Cleaning and Preprocessing
For data cleaning, columns with more than 40% missing values were dropped meaning the following three columns were dropped:\
`Electricity Use – Generated from Onsite Renewable Systems (kWh)`, `ENERGY STAR Score`, `District Hot Water Use(GJ)`.

Missing values in numerical columns, were filled with the median of their respective column and those in categorical columns were filled with the mode of their respective column.

##### Extracting and Cleaning Data Using Regex
- Regex was used to extract numeric values from text-based numeric columns (e.g., `Property GFA, Energy Use`). The following regex was used to match each group of up to 3 digits between the commas and before the decimal point in the first multiple capturing groups and then the decimal point and the digits that follow it are matched in the last capturing group\
`r"(((\d{1,3}),)*(\d{1,3})(\.\d+)?)"`\

- Regex was also used to standardize Postal Codes to follow the Canadian format (A1A 1A1). The regex used was as follows:\
`r"([A-Z][0-9][A-Z] [0-9][A-Z][0-9])"`\

- To clean text from the column `Address 1`, the street name was converted to a title case and the suffix was capitalized to maintain a consistent format for values in the column. The following regex was used to identify column values that were not consistently formatted:\
`r"(.+) (\w+ \w+)$"`\

After cleaning and reformating of column values, numerical columns were converted to the `float64` datatype.


#### Exploratory Data Analysis (EDA) and Aggregations
##### Insights
Analysis revealed that the property type with the highest recorded average Energy Use Intensity (EUI) was Heated Swimming Pool followed by Fitness Center/Health Club/Gym and then Distribution Center
The Other property type has the  lowest average Energy USe Intensity(EUI).

Distribution centers report a disproportionate energy consumption compared to other property types which might be due to no/inefficient energy management plans or benchmarking policies.

The total Greenhouse Gas (GHG) emissions by year for most property types have trended downward over the data collection period, however, Distribution Centers have had a year on year increase in emissions having almost 3 times their initially recorded values. Non-Refrigerated Warehouses also followed a similar trend of increasing emissions. 

The property with the highest energy consumption was the  Stoney Transit Facility which is a Distribution Center with a total consumption of 145,310.96 gigajoules($GJ$). The next largest consumer was the Municipal Complex which is an office with a total consumption of 81,224.82 $GJ$. The Stoney Transit's energy consumption makes up roughly 38% of the total energy consumption of the top 5 highest energy consuming buildings. The remaining three properties are of the type Fitness Center/Health Club/Gym and Ice/Curling Rink.

There is no clear indication of the influence of the COVID-19 lockdown measures on the energy consumption and green house gases emissions trends over that period.
