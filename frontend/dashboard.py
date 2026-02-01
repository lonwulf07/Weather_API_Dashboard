import streamlit as st
import requests

st.title("🌦 Weather API Dashboard")

city = st.text_input("Enter city name:", "Delhi")

if st.button("Get Weather"):
    if city:
        url = f"http://127.0.0.1:8000/weather/{city}"
        response = requests.get(url)
        st.write(response.text)

        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                st.error("City not found. Please check the city name and try again.")
            else:
                st.success(f"Weather in {city}:")
                st.metric("Temperature (°C)", data["temperature"])
                st.metric("Humidity (%)", data["humidity"])
                st.write("Condition:", data['weather'])
                
        else:
            st.error("Failed to retrieve data from the API.")