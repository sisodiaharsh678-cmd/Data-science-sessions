"""
Grad-CAM for the deepfake detector.
Highlights which regions of a face pushed the model toward "real" or "fake" —
often blending boundaries, unnatural skin texture, or asymmetric features.
"""

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import preprocess_input

IMG_SIZE = 224
LABELS = {0: "Fake", 1: "Real"}


def get_last_conv_layer_name(model):
    for layer in reversed(model.layers):
        try:
            shape = layer.output.shape
            if len(shape) == 4:
                return layer.name
        except AttributeError:
            continue
    raise ValueError("No conv layer found")


def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, prediction = grad_model(img_array)
        class_channel = prediction[:, 0]  # sigmoid single-output

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)

    prob_real = float(prediction[0][0])
    return heatmap.numpy(), prob_real


def overlay_gradcam(face_rgb, heatmap, alpha=0.45):
    heatmap_resized = cv2.resize(heatmap, (face_rgb.shape[1], face_rgb.shape[0]))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    overlay = cv2.addWeighted(face_rgb, 1 - alpha, heatmap_color, alpha, 0)
    return overlay


def predict_with_gradcam(face_rgb_224, model):
    """
    face_rgb_224: 224x224x3 RGB image (numpy array, uint8)
    Returns: (label, confidence, gradcam_overlay_rgb)
    """
    img_array = face_rgb_224.astype("float32")
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    last_conv = get_last_conv_layer_name(model)
    heatmap, prob_real = make_gradcam_heatmap(img_array, model, last_conv)
    overlay = overlay_gradcam(face_rgb_224, heatmap)

    label = LABELS[1] if prob_real >= 0.5 else LABELS[0]
    confidence = prob_real if prob_real >= 0.5 else 1 - prob_real

    return label, confidence, overlay


if __name__ == "__main__":
    model = load_model("deepfake_model.h5")
    sample = cv2.imread("00125.jpg")
    sample = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)
    sample = cv2.resize(sample, (IMG_SIZE, IMG_SIZE))

    label, conf, overlay = predict_with_gradcam(sample, model)
    print(f"Prediction: {label} ({conf*100:.1f}% confidence)")
    cv2.imwrite("gradcam_output.jpg", cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

