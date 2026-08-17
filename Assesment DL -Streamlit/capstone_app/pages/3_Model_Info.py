import streamlit as st
import pandas as pd
import pickle
import tensorflow as tf
import plotly.graph_objects as go

st.set_page_config(page_title="Model Info", layout="wide")
st.title("🧠 Model Info")

MODEL_PATH = "demand_model.keras"
HISTORY_PATH = "training_history.pkl"


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


# ---------------------------------------------------------
# Architecture summary as a formatted table
# ---------------------------------------------------------
st.subheader("Model Architecture")

try:
    model = load_model()

    layer_rows = []
    total_params = 0
    for layer in model.layers:
        try:
            output_shape = layer.output.shape
        except AttributeError:
            output_shape = "N/A"
        n_params = layer.count_params()
        total_params += n_params
        layer_rows.append({
            "Layer Name": layer.name,
            "Type": layer.__class__.__name__,
            "Output Shape": str(output_shape),
            "Parameters": f"{n_params:,}"
        })

    arch_df = pd.DataFrame(layer_rows)
    st.table(arch_df)
    st.metric("Total Parameters", f"{total_params:,}")

except Exception as e:
    st.error(
        f"Failed to load model file '{MODEL_PATH}': {e}. "
        "Make sure the trained model has been saved and placed in this app's folder."
    )

st.divider()

# ---------------------------------------------------------
# Training history: accuracy & loss line charts
# ---------------------------------------------------------
st.subheader("Training History")

try:
    with open(HISTORY_PATH, "rb") as f:
        history = pickle.load(f)

    epochs = list(range(1, len(history["accuracy"]) + 1))

    # Accuracy chart
    fig_acc = go.Figure()
    fig_acc.add_trace(go.Scatter(
        x=epochs, y=history["accuracy"], mode="lines", name="Training Accuracy"
    ))
    fig_acc.add_trace(go.Scatter(
        x=epochs, y=history["val_accuracy"], mode="lines", name="Validation Accuracy"
    ))
    fig_acc.update_layout(
        title="Training vs Validation Accuracy",
        xaxis_title="Epoch",
        yaxis_title="Accuracy"
    )
    st.plotly_chart(fig_acc, use_container_width=True)

    # Loss chart
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(
        x=epochs, y=history["loss"], mode="lines", name="Training Loss"
    ))
    fig_loss.add_trace(go.Scatter(
        x=epochs, y=history["val_loss"], mode="lines", name="Validation Loss"
    ))
    fig_loss.update_layout(
        title="Training vs Validation Loss",
        xaxis_title="Epoch",
        yaxis_title="Loss"
    )
    st.plotly_chart(fig_loss, use_container_width=True)

except FileNotFoundError:
    st.warning(
        f"Training history file '{HISTORY_PATH}' not found. "
        "Run the Task 3 training notebook/script first to generate it."
    )
except Exception as e:
    st.error(f"Failed to load training history: {e}")
