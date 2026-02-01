from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os 

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY") 

@app.get("/")
def home():
    return {"message": "Weather API is running"}

@app.get("/weather/{city}")
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "City not found"}
    
    data = response.json()
    
    result = {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"]
    }
    
    return result