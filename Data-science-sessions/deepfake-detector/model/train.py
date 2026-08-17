"""
Deepfake / AI-Generated Face Detector - Training Script
----------------------------------------------------------
Dataset: "140k Real and Fake Faces" (Kaggle)
https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces

Real faces: sourced from Flickr (FFHQ)
Fake faces: StyleGAN-generated

Expected folder structure after download:
    data/
        train/
            real/
            fake/
        valid/
            real/
            fake/
        test/
            real/
            fake/

Architecture: Xception (ImageNet pretrained) + custom classification head.
Xception is a strong choice here because deepfake artifacts often show up as
subtle high-frequency inconsistencies that depthwise separable convolutions
(Xception's core building block) are good at picking up.

Run:
    python train.py
"""

import os
import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# ---------------------------
# Config
# ---------------------------
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS_HEAD = 10       # phase 1: train head only, base frozen
EPOCHS_FINETUNE = 15   # phase 2: unfreeze top layers of Xception, fine-tune
DATA_DIR = "../data"
MODEL_OUT = "deepfake_model.h5"
CLASS_NAMES = ["fake", "real"]  # alphabetical order matches flow_from_directory default

# ---------------------------
# Data pipeline
# ---------------------------
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=10,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.1,
    horizontal_flip=True,
)

val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator = train_datagen.flow_from_directory(
    os.path.join(DATA_DIR, "train"),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    classes=CLASS_NAMES,
    shuffle=True,
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(DATA_DIR, "valid"),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    classes=CLASS_NAMES,
    shuffle=False,
)

# ---------------------------
# Model: Xception backbone + custom head
# ---------------------------
def build_model():
    base_model = Xception(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    base_model.trainable = False  # freeze for phase 1

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.3)(x)
    output = Dense(1, activation="sigmoid")(x)  # binary: real (1) vs fake (0)

    model = Model(inputs=base_model.input, outputs=output)
    return model, base_model


if __name__ == "__main__":
    model, base_model = build_model()

    # ---------------------------
    # Phase 1: train classification head only
    # ---------------------------
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc"),
                 tf.keras.metrics.Precision(name="precision"),
                 tf.keras.metrics.Recall(name="recall")],
    )

    callbacks_phase1 = [
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6),
    ]

    print("=== Phase 1: training classification head (base frozen) ===")
    model.fit(
        train_generator,
        epochs=EPOCHS_HEAD,
        validation_data=val_generator,
        callbacks=callbacks_phase1,
    )

    # ---------------------------
    # Phase 2: fine-tune top layers of Xception
    # ---------------------------
    print("=== Phase 2: fine-tuning top Xception layers ===")
    base_model.trainable = True
    # freeze all but the last ~30 layers
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=1e-5),  # much lower LR for fine-tuning
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc"),
                 tf.keras.metrics.Precision(name="precision"),
                 tf.keras.metrics.Recall(name="recall")],
    )

    callbacks_phase2 = [
        EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True),
        ModelCheckpoint(MODEL_OUT, monitor="val_auc", mode="max", save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-7),
    ]

    model.fit(
        train_generator,
        epochs=EPOCHS_FINETUNE,
        validation_data=val_generator,
        callbacks=callbacks_phase2,
    )

    # ---------------------------
    # Final test evaluation
    # ---------------------------
    test_generator = val_datagen.flow_from_directory(
        os.path.join(DATA_DIR, "test"),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="binary",
        classes=CLASS_NAMES,
        shuffle=False,
    )

    results = model.evaluate(test_generator)
    print(f"\nFinal Test Results:")
    for name, val in zip(model.metrics_names, results):
        print(f"  {name}: {val:.4f}")

    print(f"\nModel saved to: {MODEL_OUT}")
