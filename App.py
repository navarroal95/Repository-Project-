"""Hey alan, you can run this code by saving the file, then in the terminal typing "python -m streamlit run App.py".
When you do this, this should open a browser on your local machine. It won't be publicly accessible yet, but it helps with faster development.
When you're done checking the output, you can click back in the vscode terminal and press 'ctrl+c' to stop the program from running the web page.
"""

#import the packages we need
import streamlit as st
import pandas as pd
import plotly.express as px

#import our vehicles data
df = pd.read_csv("./vehicles_us.csv")

# Extract the manufacturer name from the model column, creating a new column called "manufacturer"
df['manufacturer'] = df['model'].str.split().str[0]

# Add the required st.header
st.header("Python Project", divider='rainbow')

st.write("The first five rows of our dataframe, with an added 'manufacturer' column:")
st.write(df.head())
st.write("Our dataframe has " + str(df.shape[0]) + " rows, and " + str(df.shape[1])+ " columns: ")
st.write("This dataset contains vehicle listings with various attributes including the model, condition, number of cylinders, fuel type, odometer reading, transmission type, vehicle type, paint color, 4WD indicator, date posted, and days listed. The listings encompass a variety of models from different manufacturers, each extracted from the model name. Vehicle conditions range from 'fair' to 'like new' and 'excellent,' indicating the quality and maintenance level of the cars. The dataset also includes critical information such as the odometer readings, which reflect the mileage of the vehicles, and the days listed, showing how long each vehicle has been on the market. The transmission types are all automatic in this sample, and vehicle types include SUVs, pickups, and sedans. This comprehensive set of attributes allows for a detailed analysis of factors influencing vehicle listings and their market dynamics.?")

# Generate a histogram of days listed
figA = px.histogram(df, x="days_listed", nbins=64, title='Days Listed Histogram')
st.plotly_chart(figA, use_container_width=True)
st.write("maximum days listed: " + str(max(df['days_listed'])))
st.write("minimum days listed: " + str(min(df['days_listed'])))
st.write("average days listed: " + str(sum(df['days_listed'])/len(df['days_listed'])))
st.write("This is a 'right-skewed' distribution. Notice the climax of this distribution is around 20, but the average number of days listed is 40. That's because of the outliers towards the right side.")

# df_small is a dataframe without prices above 100k, i do this to clean the boxplot chart and you should mention this in your analysis if you keep it like this
df_small = df[df['price'] < 100000]
figB = px.box(df_small, category_orders={"condition":["salvage", "fair", "good", "like new", "new", "excellent"]}, x="condition", y="price", title='Price Boxplot by Condition')
st.plotly_chart(figB, use_container_width=True)
st.write("""The condition with the largest spread in price is "new", with a q1 of 8.3k median of 21.8k and a q3 of 38.4k. As expected, prices tend to increase when a vehicle is in more pristine condition""")

# df_myp is a dataframe with just model year and price so we can calculate mean price for each
df_myp = df[['model_year', 'price']].groupby(['model_year']).mean().reset_index()
figC = px.bar(data_frame=df_myp, x='model_year', y="price", title='Average Price by Model Year')
st.plotly_chart(figC, use_container_width=True)
st.write("Cars tend to increase in price the newer they are. However, when a car is around 40-50 years old it has a chance to increase in price, these are antiques.This chart could be used to forecast the changes in car prices next year, or the time it takes for an antique car to appreciate in value.")

# Create a smaller dataframe with just manufacturer and price so we can calculate the mean price for each
df_mp = df[['manufacturer', 'price']].groupby(['manufacturer']).mean().sort_values(by=["price"], ascending=False).reset_index()
# Generate the plot using our grouped and sorted dataframe
figD = px.bar(data_frame=df_mp, x='manufacturer', y="price", title='Average Price by Manufacturer')
st.plotly_chart(figD, use_container_width=True)
st.write("Most expensive car manufacturer is mercededs-benz. However, this is likely because they only have one car model in this dataset.")

# I put the next lines here instead of in the 'if' statement so this processes before you check the box. This makes it run a bit faster.

# Group by manufacturer and model and calculate the mean price, then sort values by price to clean the visualization
df_mp = df[['manufacturer', 'model', 'price']].groupby(['manufacturer', 'model']).mean().sort_values(by=["price"], ascending=False).reset_index()
# Choose a color scale from px.colors
colorscale = px.colors.colorbrewer.Set1
# Generate a bar plot
figD = px.bar(data_frame=df_mp, x='model', y='price', color='manufacturer', color_discrete_sequence=px.colors.sample_colorscale(colorscale, 24), title='Average Price by Model and Manufacturer')
# Implement required checkbox
detail = st.checkbox("Detailed view")
if detail:
    st.plotly_chart(figD, use_container_width=True)
    st.write("Ford and Chevrolet have two of the three most expensive car models (from most to least expensive: mercedes-benz benze sprinter 2500, chevrolet silverado 1500 crew, ford mustang gt coupe 2d)\n    However, they also have two of the three least expensive car models (from least to most expensive: chevrolet trailblazer, ford taurus, dodge dakota)")

