#The exact prompt(s) you gave the AI tool.

# Write a Python + OpenCV program that reads a food-item image from disk and applies a 
# full processing pipeline: resize to 300x300, convert to grayscale, apply Gaussian blur 
# (kernel 5x5), and run Canny edge detection. Count and print the total number of edge 
# pixels detected using cv2.countNonZero(). Display the original colour image and the 
# final edge map side-by-side in a single named window using cv2.hconcat() or NumPy 
# concatenation. Save the edge map to disk as ai_edge_output.jpg and print a confirmation 
# message including the total edge pixel count and the saved filename.


import cv2

# Load image
image = cv2.imread("food.jpg")

# Resize to 300x300
resized = cv2.resize(image, (300, 300))

# Convert to grayscale
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Count edge pixels
edge_count = cv2.countNonZero(edges)

# Convert edges back to 3 channels so it can be concatenated with the colour image
edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# Combine side-by-side
combined = cv2.hconcat([resized, edges_bgr])

cv2.imshow("Original vs Edge Map", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("ai_edge_output.jpg", edges)
print(f"Edge pixels detected: {edge_count}")
print("Saved as ai_edge_output.jpg")


# Bug this version has (found in Step 2 testing)
# If you test this with a file that doesn't exist, cv2.imread() returns None — and the very next line, cv2.resize(image, (300,300)), crashes with a cryptic OpenCV assertion error instead of a clear message. There's no file-existence check at all. This is exactly the kind of bug the task expects you to catch by testing.

import cv2
import sys

# Load image
image_path = "food.jpg"
image = cv2.imread(image_path)

# FIX: check the image actually loaded before doing anything else
if image is None:
    print(f"Error: Could not load image at '{image_path}'. Please check the file path.")
    sys.exit()

# Resize to 300x300
resized = cv2.resize(image, (300, 300))

# Convert to grayscale
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Count edge pixels
edge_count = cv2.countNonZero(edges)

# Convert edges back to 3 channels so it can be concatenated with the colour image
edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# Combine side-by-side
combined = cv2.hconcat([resized, edges_bgr])

cv2.imshow("Original vs Edge Map", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("ai_edge_output.jpg", edges)
print(f"Edge pixels detected: {edge_count}")
print("Saved as ai_edge_output.jpg")


# Your 3-4 line submission note
 
"""The AI's original code called cv2.imread() without checking if the file actually loaded,
 so testing with an incorrect or missing file path caused a confusing OpenCV assertion crash at the resize step instead of a
 clear error. I added an if image is None: check right after loading, which prints a readable error message and exits gracefully via sys
 .exit() before any further processing happens. I confirmed the fix by testing with both a valid image and a deliberately wrong file path — the corrected version now fails cleanly with a helpful message instead of crashing."""