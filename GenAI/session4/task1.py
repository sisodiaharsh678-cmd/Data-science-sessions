import cv2
import numpy as np
import os


os.makedirs("noisy_steps", exist_ok=True) 

#load image 
image = cv2.imread("GenAI/session4/my_image.png", cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError("Could not load image — check that the path is correct and the file exists.")

image = image.astype(np.float32)

cv2.imwrite("noisy_steps/step_0.png", image.astype(np.uint8))

#add noise loop 

current_image= image.copy()

for step in range (1,11):
    noise = np.random.normal(loc=0 , scale=15 , size=image.shape)

    current_image=current_image+noise 
    current_image_to_save = np.clip(current_image, 0, 255).astype(np.uint8)

    #save 
    filename = f"noisy_steps/step_{step}.png"
    cv2.imwrite(filename, current_image_to_save)
    print(f"Saved {filename}")