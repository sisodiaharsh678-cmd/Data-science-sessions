import cv2 
import matplotlib.pyplot as plt 

original = cv2.imread("noisy_steps/step_0.png", cv2.IMREAD_GRAYSCALE)
noisy = cv2.imread("noisy_steps/step_10.png", cv2.IMREAD_GRAYSCALE)

#appply two diffrent denoising filters to the noisy image 

median_denoised = cv2.medianBlur(noisy , 3)
gussian_denoised = cv2.GaussianBlur(noisy , (5,5), 0)

#disply 

fig , axes = plt.subplots(1,4,figsize=(16,4))
titles = ["Original", "Noisy (Step 10)", "Median Blur", "Gaussian Blur"]
images = [original, noisy, median_denoised, gussian_denoised]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.savefig("denoise_comparison.png") 
plt.show()
