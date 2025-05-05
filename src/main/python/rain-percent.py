import json
import numpy as np
import tensorflow as tf
import joblib
import os

# 파일 경로 설정
SOURCE_JSON = "src/main/resources/static/data/rain-predict.json"
OUTPUT_JSON = os.path.join("src", "main", "resources", "static", "data", "rain-percent.json")  # static 경로로 저장
MODEL_PATH = "model/kbo_rainout_model.h5"
SCALER_PATH = "model/scaler.pkl"

# 모델 및 스케일러 로드
model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# JSON 데이터 로드
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

    except Exception:
        probability = -1  # 오류 시 -1로 설정

    results.append({
        "date": game["date"],
        "home": game["home"],
        "away": game["away"],
        "probability": probability
    })

# JSON 저장
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
