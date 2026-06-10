from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import joblib
import numpy as np

from aqi_calculator import calculate_aqi, get_aqi_category

# -----------------------------
# CONFIG
# -----------------------------
# OPENWEATHER_API_KEY = "5555555555555555555"

app = Flask(__name__)
CORS(app)

# -----------------------------
# LOAD ML MODELS
# -----------------------------
cluster_model = joblib.load("aqi_cluster_model.pkl")
cluster_scaler = joblib.load("aqi_cluster_scaler.pkl")

CLUSTER_LABELS = {
    0: "Clean Air Pattern",
    1: "Moderate Pollution Pattern",
    2: "High Pollution Pattern",
    3: "Extreme Pollution Pattern"
}

# -----------------------------
# FETCH POLLUTION DATA
# -----------------------------
def get_pollution_data(city):
    try:
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {"q": city, "limit": 1, "appid": OPENWEATHER_API_KEY}
        geo_response = requests.get(geo_url, params=geo_params).json()

        if not geo_response:
            return None

        lat = geo_response[0]["lat"]
        lon = geo_response[0]["lon"]

        pollution_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        pollution_params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY}
        pollution_response = requests.get(pollution_url, params=pollution_params).json()

        components = pollution_response["list"][0]["components"]

        return {
            "PM2.5": components["pm2_5"],
            "PM10": components["pm10"],
            "NO2": components["no2"],
            "SO2": components["so2"],
            "CO": components["co"] / 1000,
            "O3": components["o3"]
        }

    except Exception as e:
        print("API error:", e)
        return None


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return jsonify({"status": "AQI backend running"})


@app.route("/calculate-aqi")
def calculate():
    city = request.args.get("city", "Delhi")

    pollutants = get_pollution_data(city)
    if pollutants is None:
        return jsonify({"error": "City not found"}), 404

    # AQI calculation
    aqi = calculate_aqi(pollutants)
    category, color = get_aqi_category(aqi)

    # ML clustering
    features = np.array([[
        pollutants["PM2.5"],
        pollutants["PM10"],
        pollutants["NO2"],
        pollutants["SO2"],
        pollutants["CO"],
        pollutants["O3"]
    ]])

    features_scaled = cluster_scaler.transform(features)
    cluster_id = cluster_model.predict(features_scaled)[0]
    cluster_label = CLUSTER_LABELS[cluster_id]
    
        # Adjust ML label using AQI
    if aqi <= 50:
        cluster_label = "Clean Air Pattern"
    elif aqi <= 100:
        cluster_label = "Moderate Pollution Pattern"
    elif aqi <= 200:
        cluster_label = "High Pollution Pattern"
    else:
        cluster_label = "Extreme Pollution Pattern"

    return jsonify({
        "city": city,
        "AQI": aqi,
        "category": category,
        "color": color,
        "ml_cluster": cluster_label,
        "pollutants": pollutants
    })




if __name__ == "__main__":
    app.run(debug=True)
