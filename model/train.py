from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd

df    = pd.read_csv("/content/landmarks_with_angles.csv")
X     = df.drop("label", axis=1).values
y     = df["label"].values

le    = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, stratify=y_enc, random_state=42
)

print(f" Training samples : {len(X_train)}")
print(f" Testing samples  : {len(X_test)}")
print(f" Features         : {X.shape[1]} (63 positions + 15 angles)")
print(f" Classes          : {len(le.classes_)}")

model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
