import streamlit as st
import seaborn as sns
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

#Import data

os.chdir(r"C:\Users\admin\OneDrive\Desktop\streamlit_dashboards")
df = pd.read_csv("swiggy.csv", encoding = "ISO-8859-1")

st.title(":bar_chart: Swiggy Delivery Dashboard")
st.markdown("##")


#Sidebar Code
selected_city = st.sidebar.selectbox("Pick the City", df["City"].unique())

# Filter data based on selected city
filtered_df = df[df["City"] == selected_city]


# TOP KPI's
# Count restaurants in the filtered DataFrame
total_restaurants =filtered_df["ID"].count()
average_delivery = int(filtered_df["Delivery time"].mean())
  # Round to nearest integer
average_rating =filtered_df["Avg ratings"].mean().round(1)
star_rating = ":star:" * int(round(average_rating, 0))

with st.expander(label="Restaurant Stats", expanded=True):
    left_column, middle_column, right_column = st.columns(3)
with left_column:
         st.subheader("Total Restaurants:")
         st.subheader(f" {total_restaurants:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Delivery Time:")
    st.subheader(f" {average_delivery} minutes")


# Apply CSS for padding and grey background
st.markdown("""
<style>
    .st-ch {
        padding: 10px; /* Adjust padding as needed */
        background-color: #f5f5f5; /* Light grey background */
    }
</style>
""", unsafe_allow_html=True)




# Get top 10 areas for the chosen city
title=f'Top 10 Areas with Most Restaurants in {selected_city}'
top_10_areas = filtered_df['Area'].value_counts().head(10)

fig1 = px.bar(
    top_10_areas,
    x=top_10_areas.index,
    y=top_10_areas.values,
    title=f'Top 10 Areas with Most Restaurants in {selected_city}',
    color=px.colors.sequential.Viridis



)

# Customize layout with black background and white text
fig1.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    font_color='white',
    xaxis_title='Area',
    yaxis_title='Number of Restaurants'
)

# Calculate popular food types in the selected city
popular_food_types = (
    filtered_df.groupby("Food type")["ID"]
    .count()
    .to_frame(name="Count")
    .reset_index()
    .sort_values(by="Count", ascending=False)
    .head(10)
)



# Create the Plotly histogram with city-specific data
fig2 = px.histogram(
    filtered_df,
    x="Price",
    title=f"Distribution of Restaurant Prices in {selected_city} on Swiggy",
    color_discrete_sequence=["red"]  # Set color to red
)

# Apply layout customizations
fig2.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)


# Create a subset DataFrame with relevant columns
heatmap_df = filtered_df[["Avg ratings", "Delivery time","Price"]]



# Create the heatmap using Plotly Express
fig3 = px.imshow(heatmap_df.corr(),
                    labels=dict(x="Feature", y="Feature", color="Correlation"),
                    x=heatmap_df.columns,
                    y=heatmap_df.columns,
                    color_continuous_scale="RdBu")
fig3.update_layout(
        title="Correlation Heatmap of Avg Ratings, Delivery Time and Price"
    )



fig4 = px.scatter(
    filtered_df,
    x="Avg ratings",
    y="Price",
    size="ID",
    color="Area",  # Corrected: Moved "color" inside the px.scatter function
    hover_name="Area",
    log_x=True,
    size_max=55,
    range_x=[2, 5],
    range_y=[0, 2000],
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_container_width=True)




from sklearn.linear_model import LinearRegression
# Define features and target variable
features = ["Delivery time", "Price"]
target = "Avg ratings"

# Create a linear regression model
model = LinearRegression()
model.fit(df[features], df[target])

# Create sidebar for prediction input
st.sidebar.header("Predict Avg Ratings")

delivery_time = st.sidebar.number_input("Delivery time", min_value=0)
price = st.sidebar.number_input("Price", min_value=0)

# Predict when button is clicked
if st.sidebar.button("Predict"):
    new_data = pd.DataFrame([[delivery_time, price]], columns=features)
    predicted_rating = model.predict(new_data)[0]
    st.success(f"Predicted Avg Rating: {predicted_rating:.2f}")





# Sort the DataFrame in descending order of "Count"
popular_food_types = popular_food_types.sort_values(by="Count", ascending=False)

# Print the top 10 with numbering and descriptions
st.header("Top 10 Restaurant Cuisines:")
for i in range(10):
    food_type = popular_food_types.iloc[i]["Food type"]
    count = popular_food_types.iloc[i]["Count"]
    st.write(f"{i+1}. {food_type} ({count} restaurants)")

