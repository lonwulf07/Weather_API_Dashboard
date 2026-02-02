import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from database import SessionLocal
from models import Weather

def train_model(city):

    db = SessionLocal()

    records = db.query(Weather)\
        .filter(Weather.city == city)\
        .order_by(Weather.timestamp)\
        .all()

    db.close()

    if len(records) < 8:
        return None

    # Build dataframe
    data = {
        "time": [],
        "temperature": []
    }

    start_time = records[0].timestamp

    for r in records:
        delta = (r.timestamp - start_time).total_seconds() / 3600  # hours
        data["time"].append(delta)
        data["temperature"].append(r.temperature)

    df = pd.DataFrame(data)

    X = df[["time"]]
    y = df["temperature"]

    # Polynomial features (degree 2 works well usually)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    # Train/Test split (80/20)
    split = int(len(X_poly) * 0.8)

    X_train, X_test = X_poly[:split], X_poly[split:]
    y_train, y_test = y[:split], y[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate accuracy
    predictions_test = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions_test)

    return model, poly, df["time"].max(), mae