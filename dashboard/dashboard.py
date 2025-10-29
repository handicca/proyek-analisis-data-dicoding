import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="dark")


def create_monthly_registered_df(df):
    monthly_registered = (
        df.resample(rule="ME", on="date").agg({"registered": "sum"}).reset_index()
    )
    monthly_registered["year"] = monthly_registered["date"].dt.year
    monthly_registered["month"] = monthly_registered["date"].dt.strftime("%b")

    return monthly_registered


def create_season_avg_df(df):
    season_avg = df.groupby("season")["total_count"].mean().reset_index()
    return season_avg


def create_weather_avg_df(df):
    weather_avg = (
        df.groupby("weathersit")["total_count"]
        .mean()
        .reindex(["Clear", "Cloudy/Mist", "Light Rain/Snow", "Heavy Rain/Snow"])
        .reset_index()
        .fillna(0)
    )

    return weather_avg


def create_user_total_df(df):
    user_total = df[["casual", "registered"]].sum()
    return user_total


all_df = pd.read_csv("./main_data.csv")

datetime_column = "date"
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)
all_df[datetime_column] = pd.to_datetime(all_df[datetime_column])

min_date = all_df["date"].min()
max_date = all_df["date"].max()

st.set_page_config(page_title="Bike Sharing Dashboard")

with st.sidebar:
    # logo
    st.image("./logo.jpg")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )


main_df = all_df[
    (all_df["date"] >= str(start_date)) & (all_df["date"] <= str(end_date))
]

monthly_registered_df = create_monthly_registered_df(main_df)
season_avg_df = create_season_avg_df(main_df)
weather_avg_df = create_weather_avg_df(main_df)
user_total_df = create_user_total_df(main_df)

st.header("Bike Sharing Analysis Dashboard 🚴‍♂️")

st.subheader("Monthly Registered Users")

col1, col2 = st.columns(2)

with col1:
    total_registered_2011 = monthly_registered_df[
        monthly_registered_df["year"] == 2011
    ]["registered"].sum()
    st.metric("Total Registered Users in 2011", value=f"{total_registered_2011:,}")


with col2:
    total_registered_2012 = monthly_registered_df[
        monthly_registered_df["year"] == 2012
    ]["registered"].sum()
    st.metric("Total Registered Users in 2012", value=f"{total_registered_2012:,}")


fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(
    data=monthly_registered_df,
    x="month",
    y="registered",
    hue="year",
    marker="o",
    linewidth=2,
    palette=["#344CB7", "#3E7B27"],
    ax=ax,
)

ax.set_title("Trend of Registered Users per Month (2011–2012)", fontsize=16)
ax.set_xlabel(None)
ax.set_ylabel("Number of Rentals by Registered Users")
ax.legend(title="Year", loc="upper left")
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

st.subheader(
    "Analysis of the Influence of Season, Weather, and Temperature on the Number of Bicycle Rentals"
)
col1, col2 = st.columns(2)

with col1:
    colors = ["orangered", "gold", "forestgreen", "royalblue"]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=season_avg_df,
        x="season",
        y="total_count",
        hue="season",
        palette=colors,
        order=["Spring", "Summer", "Fall", "Winter"],
        ax=ax,
    )

    ax.set_title("Average Total Rentals by Season", fontsize=16)
    ax.set_xlabel("Season")
    ax.set_ylabel("Average Total Rent")

    st.pyplot(fig)


with col2:
    colors = ["skyblue", "lightgrey", "lightcoral", "slateblue"]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=weather_avg_df,
        x="weathersit",
        y="total_count",
        hue="weathersit",
        palette=colors,
        ax=ax,
    )
    ax.set_title("Average Rental Rates Based on Weather Conditions")
    ax.set_xlabel("Weather Conditions")
    ax.set_ylabel("Average Total Rent")

    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 5))

sns.regplot(
    data=main_df,
    x="temp",
    y="total_count",
    scatter_kws={"alpha": 0.5},
    line_kws={"color": "red"},
    ax=ax,
)

ax.set_label("Relationship between Temperature and Rental Amount")
ax.set_xlabel("Temprature")
ax.set_ylabel("Rental Amount")

st.pyplot(fig)


st.subheader("Registered vs Casual User Dominance (2011–2012)")

fig, ax = plt.subplots(figsize=(7, 7))

colors = ["lightblue", "seagreen"]
ax.pie(
    user_total_df,
    labels=["Casual Users", "Registered Users"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    explode=(0.03, 0.03),
    textprops={"fontsize": 12},
)

st.pyplot(fig)

st.subheader(
    "Advanced Analysis: Application of Clustering Techniques with Manual Grouping Methods"
)
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#00B8A9", "#F6416C", "#FFDE7D"]
sns.countplot(
    data=main_df,
    x="activity_level",
    palette=colors,
    hue="activity_level",
    order=["Low Activity", "Medium Activity", "High Activity"],
)

ax.set_title("Distribution of Days Based on Rental Activity Level")
ax.set_xlabel(None)
ax.set_ylabel("Number of days")

st.pyplot(fig)
