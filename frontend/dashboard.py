import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    layout="wide"
)

st.title("🌦 Weather Analytics & ML Forecast Platform")

API_BASE = "https://weather-api-dashboard-7sqm.onrender.com/"

# ------------------ CURRENT WEATHER ------------------

st.header("📍 Current Weather")

col1, col2, col3 = st.columns(3)

city = st.text_input("Enter city", "Delhi")

if st.button("Fetch Weather"):

    response = requests.get(f"{API_BASE}/weather/{city}")

    if response.status_code == 200:
        data = response.json()

        if "error" in data:
            st.error("City not found")
        else:
            col1.metric("🌡 Temperature (°C)", data["temperature"])
            col2.metric("💧 Humidity (%)", data["humidity"])
            col3.metric("☁ Condition", data["weather"])
    else:
        st.error("API error")

st.divider()

# ------------------ HISTORY & ANALYTICS ------------------

st.header("📊 Historical Analytics")

if st.button("Load Historical Data"):

    response = requests.get(f"{API_BASE}/history")

    if response.status_code == 200:

        df = pd.DataFrame(response.json())

        if df.empty:
            st.warning("No data yet")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            city_filter = st.selectbox("Filter by city", df["city"].unique())

            city_df = df[df["city"] == city_filter]

            chart_col1, chart_col2 = st.columns(2)

            # Temperature chart
            with chart_col1:
                st.subheader("🌡 Temperature Trend")
                plt.figure(figsize=(6,4))
                plt.plot(city_df["timestamp"], city_df["temperature"])
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(plt)

            # Humidity chart
            with chart_col2:
                st.subheader("💧 Humidity Trend")
                plt.figure(figsize=(6,4))
                plt.plot(city_df["timestamp"], city_df["humidity"])
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(plt)

            st.subheader("📋 Raw Records")
            st.dataframe(city_df)

st.divider()

# ------------------ ML FORECAST ------------------

st.header("🤖 ML Temperature Forecast")

forecast_city = st.text_input("City for forecast", "Delhi")

if st.button("Run Forecast"):

    response = requests.get(f"{API_BASE}/forecast/{forecast_city}")

    if response.status_code == 200:
        data = response.json()

        if "error" in data:
            st.warning("Not enough historical data")
        else:
            forecast = data["forecast"]
            mae = data["mae"]

            st.success(f"Model MAE: {mae} °C")

            plt.figure(figsize=(6,4))
            plt.plot(range(1,6), forecast)
            plt.xlabel("Future Step")
            plt.ylabel("Temperature")
            plt.tight_layout()
            st.pyplot(plt)

            st.write("### Forecast Values")
            for i, temp in enumerate(forecast, 1):
                st.write(f"Step {i}: {round(temp,2)} °C")

    else:
        st.error("Forecast API error")

st.divider()

st.caption("Built with FastAPI • Streamlit • SQLite • Scikit-learn")