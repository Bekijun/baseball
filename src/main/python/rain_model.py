import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import joblib

# CSV 불러오기
df = pd.read_csv("data/rain_data.csv")

# 특징 컬럼과 라벨 설정
features = ['3-시간', '2-시간', '1-시간', '0시간', '1시간', '2시간']
df["누적 강수량"] = df[features].sum(axis=1)

X = df[features + ["누적 강수량"]]
y = df['비고']

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "model/scaler.pkl")  # 스케일러 저장

# 학습용 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 모델 구성
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 학습 수행
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_data=(X_test, y_test))

# 모델 저장
model.save("model/kbo_rainout_model.h5")
print("✅ 모델 저장 완료")
