from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os 

from database import SessionLocal, engine
from models import Weather, Base

from ml_model import train_model
import numpy as np

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY") 

#Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Weather API with DB is running"}

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
    
    # Save to database
    db = SessionLocal()
    
    weather_record = Weather(
        city=city,
        temperature=result["temperature"],
        humidity=result["humidity"],
        condition=result["weather"]
    )
    
    db.add(weather_record)
    db.commit()
    db.close()
    
    return result

@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(Weather).order_by(Weather.timestamp.desc()).all()
    db.close()
    
    return records

@app.get("/forecast/{city}")
def forecast(city: str):

    trained = train_model(city)

    if trained is None:
        return {"error": "Not enough data to forecast"}

    model, poly, last_time, mae = trained

    # Predict next 5 hours (or steps)
    future_times = np.array([
        last_time + i for i in range(1, 6)
    ]).reshape(-1, 1)

    future_poly = poly.transform(future_times)

    predictions = model.predict(future_poly)

    return {
        "city": city,
        "forecast": predictions.tolist(),
        "mae": round(mae, 2)   # model accuracy metric
    }
