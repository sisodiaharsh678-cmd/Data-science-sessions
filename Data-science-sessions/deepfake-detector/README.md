# AI-Generated / Deepfake Face Detector (Xception Transfer Learning + Grad-CAM)

A binary classifier that distinguishes real photographs from AI-generated
(StyleGAN) faces, using transfer learning on Xception with a two-phase
fine-tuning strategy, and Grad-CAM explainability to visualize what the
model detects as "fake."

## Features
- Transfer learning on **Xception** (ImageNet pretrained), fine-tuned in two phases
- Trained on **140k Real and Fake Faces** dataset
- Full evaluation suite: confusion matrix, ROC-AUC, precision-recall curve
- Grad-CAM heatmaps showing which facial regions drove each prediction
- Deployed as an interactive Streamlit app (upload an image, get Real/Fake + confidence + heatmap)

## Tech Stack
Python, TensorFlow/Keras, Xception (transfer learning), OpenCV, Streamlit, scikit-learn

## Project Structure
```
deepfake-detector/
├── data/                       # dataset (train/valid/test, download separately)
├── model/
│   ├── train.py                 # two-phase Xception training
│   ├── evaluate.py               # confusion matrix, ROC, PR curve
│   ├── gradcam.py                # Grad-CAM explainability
│   └── deepfake_model.h5         # trained model (generated after training)
├── app/
│   └── streamlit_app.py          # deployed web app
├── requirements.txt
└── README.md
```

## Setup — Step by Step

### 1. Environment
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux

pip install -r requirements.txt
```

### 2. Download the dataset
**140k Real and Fake Faces** (Kaggle):
https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces

Extract so you have:
```
data/train/real/, data/train/fake/
data/valid/real/, data/valid/fake/
data/test/real/,  data/test/fake/
```
(The Kaggle dataset already ships with this split — you shouldn't need to
re-split it manually.)

### 3. Train the model
```bash
cd model
python train.py
```
Two phases:
- **Phase 1** (~10 epochs): base frozen, train the classification head only
- **Phase 2** (~15 epochs): unfreeze top 30 Xception layers, fine-tune at low LR

On CPU (Mac M-series) this will be slow — realistically 4-8+ hours given
Xception's size and 140k images. **Strongly recommend using Google Colab
with a free GPU runtime** for this one; expect 45-90 minutes total on a
T4 GPU. If you want to move faster, use a subset of the dataset (e.g., 20k
images) for a first working version, then scale up.

### 4. Evaluate
```bash
python evaluate.py
```
Produces `confusion_matrix.png`, `roc_curve.png`, `precision_recall_curve.png`,
plus a full classification report in the terminal.

**Why recall matters more here:** a false negative (fake image classified as
real) is a worse failure mode than a false positive (real image flagged for
review). Mention this tradeoff explicitly in interviews — it shows you think
about metrics in context, not just chasing accuracy.

### 5. Test Grad-CAM on a single image
```bash
python gradcam.py
```

### 6. Launch the Streamlit app
```bash
cd ../app
streamlit run streamlit_app.py
```

## Deploying Publicly (Streamlit Community Cloud)
1. Push to GitHub — use Git LFS for `deepfake_model.h5` (Xception-based models
   run 80-100MB+, over GitHub's normal file size comfort zone)
2. Go to share.streamlit.io, connect your repo
3. Main file path: `app/streamlit_app.py`
4. Deploy — get a public demo URL for your resume/LinkedIn

## Results (fill in after training)
| Metric | Value |
|---|---|
| Test Accuracy | ~XX% |
| Test AUC | ~XX |
| Recall (fake class) | ~XX% |

## Resume Bullet Points (use after you have real numbers)
- Built an AI-generated face detector using transfer learning on Xception
  (ImageNet pretrained), fine-tuned in two phases on 140k real/StyleGAN-fake
  face images, achieving XX% accuracy and XX AUC
- Prioritized recall on the "fake" class over raw accuracy, reflecting the
  higher cost of false negatives in a misinformation-detection context
- Implemented Grad-CAM to visualize model attention on blending artifacts
  and texture inconsistencies, improving interpretability for non-technical review
- Deployed as an interactive Streamlit web app for real-time image verification

## Honest Limitations (know these for interviews)
- Trained only on **GAN-generated** (StyleGAN) fakes — performance on newer
  **diffusion-based** generators (Midjourney, DALL-E 3, Stable Diffusion) is
  untested and likely weaker, since those produce different artifact signatures
- Face-only detection — doesn't handle full-scene deepfakes or video deepfakes
  (temporal consistency checks, which video deepfake detection needs, aren't covered)
- Natural "next step" to mention in interviews: extend training data to
  include diffusion-generated fakes, and explore frequency-domain features
  (DCT/FFT-based artifacts) as an additional signal alongside the CNN

## Notes on Known Issues (from your TOPS environment)
- OpenCV 5.x breaking changes: use `opencv-python==4.10.0.84`
- Mac M-series: consider `tensorflow-macos` + `tensorflow-metal` for GPU
  acceleration, though Colab GPU is strongly recommended for this project
  given Xception's size
