import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
import tensorflow as tf
import joblib

df = pd.read_csv("data/rain_data.csv")

features = ['3-시간', '2-시간', '1-시간', '0시간', '1시간', '2시간']
df["누적 강수량"] = df[features].sum(axis=1)
feature_cols = features + ["누적 강수량"]
X = df[feature_cols]
y = df["비고"]

if y.dtype == object:
    y = y.map({"O": 1, "X": 0})

X = X.dropna()
y = y.loc[X.index]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)
joblib.dump(scaler, "model/scaler.pkl")

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled_df, y, test_size=0.2, random_state=42, stratify=y
)

class_weights = class_weight.compute_class_weight(
    class_weight="balanced", classes=np.unique(y_train), y=y_train
)
class_weights = dict(enumerate(class_weights))
print("클래스 가중치:", class_weights)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=8,
    validation_data=(X_test, y_test),
    class_weight=class_weights
)

model.save("model/kbo_rainout_model.h5")
print("모델 저장 완료")
