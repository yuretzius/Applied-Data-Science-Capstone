# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

# Exploratory Data Analysis

# First, let's read the SpaceX dataset into a Pandas dataframe and print its summary

# URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"

df=pd.read_csv("dataset_part_2.csv")
print(df.head(5))

# First, let's try to see how the FlightNumber (indicating the continuous launch attempts.) and Payload variables would affect the launch outcome.

# We can plot out the FlightNumber vs. PayloadMassand overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass also appears to be a factor; even with more massive payloads, the first stage often returns successfully.

custom_palette = {
    1: "green",
    0: "red"
}


sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", palette=custom_palette, data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# Next, let's drill down to each site visualize its detailed launch records.

# TASK 1: Visualize the relationship between Flight Number and Launch Site

# Use the function catplot to plot FlightNumber vs LaunchSite, set the parameter x parameter to FlightNumber,set the y to Launch Site and set the parameter hue to 'class'

# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value

sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", palette=custom_palette, data=df, aspect = 1.5 ,height=5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Launch Site",fontsize=20)
plt.show()

# Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.

# TASK 2: Visualize the relationship between Payload Mass and Launch Site

# We also want to observe if there is any relationship between launch sites and their payload mass.

# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value
sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", palette=custom_palette, data=df, aspect = 1.5 ,height=6)
plt.xlabel("Pay load Mass (kg)",fontsize=20)
plt.ylabel("Launch Site",fontsize=20)
plt.show()

# Now if you observe Payload Mass Vs. Launch Site scatter point chart you will find for the VAFB-SLC launchsite there are no rockets launched for heavypayload mass(greater than 10000).

# TASK 3: Visualize the relationship between success rate of each orbit type

# Next, we want to visually check if there are any relationship between success rate and orbit type.

# Let's create a bar chart for the sucess rate of each orbit

# HINT use groupby method on Orbit column and get the mean of Class column
sr_df = df.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
sr_df['Class'] = sr_df['Class'] * 100

sns.barplot(data=sr_df, x='Orbit', y='Class')
plt.xlabel('Orbit')
plt.ylabel('Class (Success Rate (%))')
plt.show()

# Analyze the plotted bar chart to identify which orbits have the highest success rates.

# TASK 4: Visualize the relationship between FlightNumber and Orbit type

# For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.

# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value

sns.catplot(x="FlightNumber", y="Orbit", hue="Class", palette=custom_palette, data=df, aspect = 1.5 ,height=6)

plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Orbit",fontsize=20)
plt.show()

# You can observe that in the LEO orbit, success seems to be related to the number of flights. Conversely, in the GTO orbit, there appears to be no relationship between flight number and success.

# TASK 5: Visualize the relationship between Payload Mass and Orbit type

# Similarly, we can plot the Payload Mass vs. Orbit scatter point charts to reveal the relationship between Payload Mass and Orbit type

# Plot a scatter point chart with x axis to be Payload Mass and y axis to be the Orbit, and hue to be the class value

sns.catplot(x="PayloadMass", y="Orbit", hue="Class", palette=custom_palette, data=df, aspect = 1.5 ,height=6)

plt.xlabel("Pay load Mass (kg)",fontsize=20)
plt.ylabel("Orbit",fontsize=20)
plt.show()

# With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.

# However, for GTO, it's difficult to distinguish between successful and unsuccessful landings as both outcomes are present.

# TASK 6: Visualize the launch success yearly trend

# You can plot a line chart with x axis to be Year and y axis to be average success rate, to get the average launch success trend.

# The function will help you get the year from the date:

# A function to Extract years from the date 

year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
print(df.head())

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate

sns.lineplot(data=df, x="Date", y="Class")
plt.xlabel("Year")
plt.ylabel("Success Rate")
plt.show()

# you can observe that the sucess rate since 2013 kept increasing till 2020

# Features Engineering

# By now, you should obtain some preliminary insights about how each important variable would affect the success rate, we will select the features that will be used in success prediction in the future module.

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
print(features.head())

# TASK 7: Create dummy variables to categorical columns

# Use the function get_dummies and features dataframe to apply OneHotEncoder to the column Orbits, LaunchSite, LandingPad, and Serial. Assign the value to the variable features_one_hot, display the results using the method head. Your result dataframe must include all features including the encoded ones.

# HINT: Use get_dummies() function on the categorical columns
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
print(features_one_hot.head())

# TASK 8: Cast all numeric columns to float64

# Now that our features_one_hot dataframe only contains numbers, cast the entire dataframe to variable type float64

# HINT: use astype function
features_one_hot1 = features_one_hot.astype('float64')

# We can now export it to a CSV for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.

features_one_hot1.to_csv('dataset_part_3.csv', index=False)

print(features_one_hot1)




    











