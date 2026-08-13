import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os

# Load trained YOLO model
model = YOLO("best.pt")

st.title("License Plate Detection App")

# Two options: Upload image OR use sample
option = st.radio("Choose input method:", ("Upload Image", "Sample Image"))

image = None

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Check file extension
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext in [".jpg", ".jpeg", ".png"]:
            image = Image.open(uploaded_file).convert("RGB")
        else:
            st.error("❌ Invalid file type. Please upload a JPG, JPEG, or PNG image.")

elif option == "Sample Image":
    sample_dir = "car_images"  # Folder with sample images
    sample_images = os.listdir(sample_dir)

    # Add a default "Select an image" option
    selected_sample = st.selectbox("Choose a sample image:", ["Select an image"] + sample_images)

    if selected_sample != "Select an image":
        image_path = os.path.join(sample_dir, selected_sample)
        image = Image.open(image_path).convert("RGB")

# Run detection only if an image is selected/loaded
if image is not None:
    st.image(image, caption="Input Image", use_container_width=True)

    # Run YOLO prediction
    results = model.predict(image)

    # Show YOLO annotated result (convert BGR -> RGB)
    for r in results:
        bgr_img = r.plot()  
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        st.image(rgb_img, caption="YOLO Detection", use_container_width=True)

        # Extract bounding boxes and crop license plates
        boxes = r.boxes.xyxy.cpu().numpy()
        if len(boxes) > 0:
            st.subheader("Detected Plates:")
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)
                cropped_plate = np.array(image)[y1:y2, x1:x2]  # already RGB
                st.image(cropped_plate, caption=f"Plate {i+1}")
        else:
            st.warning("No license plate detected.")
