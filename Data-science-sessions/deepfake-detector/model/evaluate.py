"""
Evaluate the trained deepfake detector.
Produces: classification report, confusion matrix, ROC curve (AUC).

Note on metric priority for this task:
Recall on "fake" matters more than raw accuracy — missing a deepfake (false
negative) is a worse outcome than flagging a real photo for review (false
positive). Report and explain this tradeoff in interviews.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve
)

IMG_SIZE = 224
BATCH_SIZE = 32
DATA_DIR = "../data"
CLASS_NAMES = ["fake", "real"]

model = load_model("deepfake_model.h5")

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_generator = test_datagen.flow_from_directory(
    f"{DATA_DIR}/test",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    classes=CLASS_NAMES,
    shuffle=False,
)

probs = model.predict(test_generator).ravel()
y_pred = (probs >= 0.5).astype(int)
y_true = test_generator.classes

# ---------------------------
# Classification report
# ---------------------------
print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))

# ---------------------------
# Confusion matrix
# ---------------------------
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Deepfake Detection")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
print("Saved confusion_matrix.png")

# ---------------------------
# ROC curve
# ---------------------------
fpr, tpr, _ = roc_curve(y_true, probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Deepfake Detection")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("roc_curve.png", dpi=150)
print(f"Saved roc_curve.png (AUC = {roc_auc:.3f})")

# ---------------------------
# Precision-Recall curve (more informative than ROC for imbalanced-feel tasks)
# ---------------------------
precision, recall, _ = precision_recall_curve(y_true, probs)
plt.figure(figsize=(6, 5))
plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve - Deepfake Detection")
plt.tight_layout()
plt.savefig("precision_recall_curve.png", dpi=150)
print("Saved precision_recall_curve.png")
