# model/train.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd
import os
import time

# ── Load data ─────────────────────────────────────
df    = pd.read_csv("data/Arabic_Sign_Language_Letters_Dataset.csv")
X     = df.drop("label", axis=1).values
y     = df["label"].values

le    = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, stratify=y_enc, random_state=42
)

print(f"Training samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}")
print(f"Features         : {X.shape[1]} (63 positions + 15 angles)")
print(f"Classes          : {len(le.classes_)}")

# ── Train ─────────────────────────────────────────
print("\n⏳ Training...")
start = time.time()

model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

elapsed = time.time() - start
print(f"✅ Training done in {elapsed:.1f} seconds")

# ── Evaluate ────────────────────────────────────── 
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Accuracy: {accuracy * 100:.2f}%")
print("\n📊 Per-letter report:")
print(classification_report(
    y_test, y_pred,
    target_names=le.classes_
))

# ── Speed test ────────────────────────────────────  
sample = X[0:1]
t = time.time()
for _ in range(100):
    model.predict(sample)
ms = (time.time() - t) / 100 * 1000
print(f"⚡ Prediction speed: {ms:.2f}ms per frame")

# ── Save ──────────────────────────────────────────  
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/sign_model.pkl")
joblib.dump(le,    "model/label_encoder.pkl")
print("\n✅ model/sign_model.pkl saved")
print("✅ model/label_encoder.pkl saved")
