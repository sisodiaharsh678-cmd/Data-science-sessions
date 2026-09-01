import streamlit as st
import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "model"))
from gradcam import predict_with_gradcam  # noqa: E402

st.set_page_config(
    page_title="Deepfake Face Detector",
    page_icon="🕵️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

MODEL_PATH = "../model/deepfake_model.h5"
IMG_SIZE = 224

# ---------------------------------------------------------------
# Custom theme / CSS
# ---------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f1117 0%, #171a23 100%);
    }

    .hero {
        text-align: center;
        padding: 1.6rem 1rem 1.2rem 1rem;
    }
    .hero h1 {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7f77dd, #d4537e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #9c9a92;
        font-size: 0.98rem;
        max-width: 560px;
        margin: 0 auto;
        line-height: 1.5;
    }

    .badge-row { text-align: center; margin: 0.8rem 0 1.4rem 0; }
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(127,119,221,0.15);
        color: #b4aef0;
        border: 1px solid rgba(127,119,221,0.35);
    }

    .result-card {
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin: 1rem 0;
        border: 1px solid;
    }
    .result-fake {
        background: rgba(226,75,74,0.08);
        border-color: rgba(226,75,74,0.4);
    }
    .result-real {
        background: rgba(99,153,34,0.08);
        border-color: rgba(99,153,34,0.4);
    }
    .result-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .result-fake .result-title { color: #f09595; }
    .result-real .result-title { color: #97c459; }
    .result-sub { color: #9c9a92; font-size: 0.9rem; }

    .conf-bar-bg {
        width: 100%; height: 8px; border-radius: 999px;
        background: rgba(255,255,255,0.08); margin-top: 0.8rem; overflow: hidden;
    }
    .conf-bar-fill { height: 100%; border-radius: 999px; }

    .disclaimer-box {
        background: rgba(239,159,39,0.08);
        border: 1px solid rgba(239,159,39,0.3);
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        font-size: 0.85rem;
        color: #e0b96e;
        margin-top: 1rem;
        line-height: 1.5;
    }

    section[data-testid="stFileUploaderDropzone"] {
        border-radius: 14px;
        border: 1.5px dashed rgba(127,119,221,0.4) !important;
        background: rgba(127,119,221,0.04);
    }

    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_model():
    return load_model(MODEL_PATH)


model = get_model()

# ---------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🕵️ Deepfake Face Detector</h1>
    <p>A fine-tuned Xception CNN with Grad-CAM explainability — upload a face photo
    to see whether it's a real photograph or an AI-generated fake, and exactly
    which regions drove the decision.</p>
</div>
<div class="badge-row">
    <span class="badge">Transfer Learning</span>
    <span class="badge">Xception</span>
    <span class="badge">Grad-CAM</span>
    <span class="badge">TensorFlow / Keras</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍  Detect", "📊  Model Info"])

# ---------------------------------------------------------------
# Tab 1 — Detect
# ---------------------------------------------------------------
with tab1:
    uploaded = st.file_uploader("Upload a face photo", type=["jpg", "jpeg", "png"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        img_array = np.array(image)
        face_resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))

        with st.spinner("Analyzing facial regions..."):
            label, confidence, overlay = predict_with_gradcam(face_resized, model)

        col1, col2 = st.columns(2)
        with col1:
            st.image(face_resized, caption="Input image", use_container_width=True)
        with col2:
            st.image(overlay, caption="Grad-CAM — model attention", use_container_width=True)

        conf_pct = confidence * 100
        is_fake = label == "Fake"
        css_class = "result-fake" if is_fake else "result-real"
        bar_color = "#e24b4a" if is_fake else "#639922"
        icon = "⚠️" if is_fake else "✅"
        headline = "Likely AI-generated" if is_fake else "Likely a real photo"

        st.markdown(f"""
        <div class="result-card {css_class}">
            <div class="result-title">{icon} {headline}</div>
            <div class="result-sub">Model confidence: {conf_pct:.1f}%</div>
            <div class="conf-bar-bg">
                <div class="conf-bar-fill" style="width:{conf_pct:.1f}%; background:{bar_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer-box">
            <strong>Scope note:</strong> this model was trained on original StyleGAN-generated
            faces. Testing shows it does not reliably generalize to newer generators
            (StyleGAN2/3, diffusion models like Midjourney or Stable Diffusion) — those may be
            misclassified as real. Not intended as a sole source of truth for high-stakes verification.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Upload a photo above to get started — or try one of your own test images.")

# ---------------------------------------------------------------
# Tab 2 — Model Info
# ---------------------------------------------------------------
with tab2:
    st.subheader("Architecture")
    st.code(
        "Xception (ImageNet pretrained, top removed)\n"
        "-> GlobalAveragePooling2D\n"
        "-> Dense(256) + BatchNorm + Dropout(0.5)\n"
        "-> Dense(64) + Dropout(0.3)\n"
        "-> Dense(1, sigmoid)  [Real vs Fake]",
        language="text",
    )

    st.subheader("Training strategy")
    st.write(
        "**Phase 1 — Feature extraction:** Xception base frozen, only the "
        "classification head trains (up to 10 epochs).\n\n"
        "**Phase 2 — Fine-tuning:** top 30 Xception layers unfrozen, trained "
        "jointly with the head at a much lower learning rate (1e-5) for up to "
        "15 epochs — adapting high-level features without destroying pretrained knowledge."
    )

    st.subheader("Dataset")
    st.write(
        "140,000 images — real faces from FFHQ (Flickr), fake faces generated by "
        "original StyleGAN. Split into train / valid / test."
    )

    st.subheader("Why Xception?")
    st.write(
        "Deepfake artifacts often show up as subtle high-frequency inconsistencies — "
        "unnatural pore texture, blending boundaries, slight asymmetries. Xception's "
        "depthwise separable convolutions are efficient at capturing this kind of "
        "fine-grained spatial detail, which is why it's a common backbone choice in "
        "deepfake detection research."
    )

    st.caption("Built with TensorFlow / Keras, OpenCV, and Streamlit.")