from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

y_pred = model.predict(X_test)

print(f"\n Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred, target_names=le.classes_))
 import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

plt.figure(figsize=(20, 16))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm,
            annot=True, fmt="d",
            xticklabels=le.classes_,
            yticklabels=le.classes_,
            cmap="Blues",
            linewidths=0.5,
            annot_kws={"size": 9})
plt.title("Confusion Matrix — Arabic Sign Language (Random Forest)",
          fontsize=18, pad=20)
plt.xlabel("Predicted Label", fontsize=13)
plt.ylabel("True Label",      fontsize=13)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(rotation=0,  fontsize=10)

report    = classification_report(y_test, y_pred,
                                  target_names=le.classes_,
                                  output_dict=True)
report_df = pd.DataFrame(report).T
report_df = report_df.drop(["accuracy", "macro avg", "weighted avg"])

plt.figure(figsize=(16, 7))
colors = ["#e74c3c" if f < 0.80 else
          "#f39c12" if f < 0.90 else
          "#2ecc71"
          for f in report_df["f1-score"]]

bars = plt.bar(report_df.index, report_df["f1-score"],
               color=colors, edgecolor="white", width=0.6)

for bar, val in zip(bars, report_df["f1-score"]):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.008,
             f"{val:.2f}",
             ha="center", va="bottom", fontsize=8.5, fontweight="bold")

plt.axhline(y=0.90, color="gray",    linestyle="--", linewidth=1.2, label="90% line")
plt.axhline(y=0.80, color="#e74c3c", linestyle="--", linewidth=1.2, label="80% line")

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2ecc71", label="Strong  (≥ 90%)"),
    Patch(facecolor="#f39c12", label="OK      (80–90%)"),
    Patch(facecolor="#e74c3c", label="Weak    (< 80%)")
]
plt.legend(handles=legend_elements, fontsize=10, loc="lower right")
plt.title("F1-Score per Arabic Sign Class", fontsize=15, pad=15)
plt.xlabel("Sign Class", fontsize=12)
plt.ylabel("F1-Score",   fontsize=12)
plt.ylim(0, 1.12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.tight_layout()
plt.savefig("/content/drive/MyDrive/Sign Bridge/f1_per_class.png", dpi=150)
plt.show()

fig, ax = plt.subplots(figsize=(20, 7))
x     = np.arange(len(report_df))
width = 0.26

ax.bar(x - width, report_df["precision"], width,
       label="Precision", color="#3498db", edgecolor="white")
ax.bar(x,          report_df["recall"],   width,
       label="Recall",    color="#2ecc71", edgecolor="white")
ax.bar(x + width,  report_df["f1-score"], width,
       label="F1-Score",  color="#e67e22", edgecolor="white")

ax.set_xticks(x)
ax.set_xticklabels(report_df.index, rotation=45, ha="right", fontsize=10)
ax.set_ylim(0, 1.15)
ax.set_title("Precision / Recall / F1-Score per Arabic Sign", fontsize=15, pad=15)
ax.set_ylabel("Score", fontsize=12)
ax.legend(fontsize=11)
ax.axhline(y=0.90, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax.yaxis.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/content/drive/MyDrive/Sign Bridge/precision_recall_f1.png", dpi=150)
plt.show()

importances = model.feature_importances_
feat_names  = df.drop("label", axis=1).columns.tolist()

feat_df = pd.DataFrame({
    "feature":    feat_names,
    "importance": importances
}).sort_values("importance", ascending=False).head(20)

plt.figure(figsize=(12, 8))
sns.barplot(data=feat_df, x="importance", y="feature", palette="viridis")
plt.title("Top 20 Most Important Hand Landmarks", fontsize=14, pad=15)
plt.xlabel("Importance Score", fontsize=12)
plt.ylabel("Feature",          fontsize=12)
plt.tight_layout()
plt.savefig("/content/drive/MyDrive/Sign Bridge/feature_importance.png", dpi=150)
plt.show()

class_counts = df["label"].value_counts().sort_index()

plt.figure(figsize=(16, 6))
bars = plt.bar(class_counts.index, class_counts.values,
               color="#5dade2", edgecolor="white")

for bar, val in zip(bars, class_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             str(val), ha="center", va="bottom", fontsize=8)

plt.axhline(y=class_counts.mean(), color="red", linestyle="--",
            linewidth=1.5, label=f"Mean: {class_counts.mean():.0f}")
plt.title("Number of Samples per Class", fontsize=14, pad=15)
plt.xlabel("Sign Class", fontsize=12)
plt.ylabel("Sample Count", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig("/content/drive/MyDrive/Sign Bridge/samples_per_class.png", dpi=150)
plt.show()

best_sign  = report_df["f1-score"].idxmax()
worst_sign = report_df["f1-score"].idxmin()

print("=" * 45)
print("      SIGN BRIDGE — MODEL SUMMARY")
print("=" * 45)
print(f"  Total samples       : {len(df)}")
print(f"  Features per sample : {X.shape[1]} (63 positions + 15 angles)")
print(f"  Classes             : {len(le.classes_)}")
print(f"  Train / Test split  : 80% / 20%")
print("-" * 45)
print(f"  Overall Accuracy    : {accuracy_score(y_test, y_pred):.2%}")
print(f"  Macro Precision     : {report['macro avg']['precision']:.2%}")
print(f"  Macro Recall        : {report['macro avg']['recall']:.2%}")
print(f"  Macro F1-Score      : {report['macro avg']['f1-score']:.2%}")
print("-" * 45)
print(f"  Best  sign : {best_sign:<15} F1 = {report_df['f1-score'].max():.2%}")
print(f"  Worst sign : {worst_sign:<15} F1 = {report_df['f1-score'].min():.2%}")
print("=" * 45)
plt.tight_layout()
plt.savefig("/content/drive/MyDrive/Sign Bridge/confusion_matrix.png", dpi=150)
plt.show()
