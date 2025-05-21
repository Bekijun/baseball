import json
import numpy as np
import tensorflow as tf
import joblib
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_JSON = os.path.join(BASE_DIR, "main", "resources", "static", "data", "rain-predict.json")
OUTPUT_JSON = os.path.join(BASE_DIR, "main", "resources", "static", "data", "rain-percent.json")
MODEL_PATH = os.path.join(BASE_DIR, "main", "python", "model", "kbo_rainout_model.h5")
SCALER_PATH = os.path.join(BASE_DIR, "main", "python", "model", "scaler.pkl")

model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

with open(SOURCE_JSON, "r", encoding="utf-8") as f:
    game_data = json.load(f)

results = []

for game in game_data:
    try:
        rain_values = [
            float(w["rain"]) if w["rain"] not in ["-", "", None] else 0.0
            for w in game.get("weather", [])
        ]

        if len(rain_values) < 6:
            raise ValueError("강수량 데이터 부족")

        features = rain_values[:6] + [sum(rain_values[:6])]
        scaled = scaler.transform([features])
        prediction = model.predict(scaled)
        probability = round(float(prediction[0][0]) * 100, 2)

    except Exception as e:
        probability = -1

    results.append({
        "date": game["date"],
        "home": game["home"],
        "away": game["away"],
        "probability": probability
    })

os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

