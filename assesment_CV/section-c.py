import cv2
import os
import sys

# Global variable to hold the currently loaded image
image = None
image_path = None


def load_and_inspect():
    global image, image_path

    path = input("Enter the image file path: ").strip()
    img = cv2.imread(path)

    if img is None:
        print("Error: Image not found. Please check the file path.")
        return

    image = img
    image_path = path

    height, width, channels = image.shape
    print(f"Height: {height}")
    print(f"Width: {width}")
    print(f"Channels: {channels}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Original", image)
    cv2.imshow("Grayscale", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    base_name = os.path.splitext(os.path.basename(path))[0]
    gray_filename = f"{base_name}_gray.jpg"
    cv2.imwrite(gray_filename, gray)
    print(f"Grayscale image saved as {gray_filename}")


def resize_and_analyse():
    if image is None:
        print("No image loaded yet. Please use Option 1 first.")
        return

    resized = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)

    B, G, R = cv2.split(resized)

    b_avg = round(B.mean(), 2)
    g_avg = round(G.mean(), 2)
    r_avg = round(R.mean(), 2)

    print(f"Average Blue Intensity: {b_avg}")
    print(f"Average Green Intensity: {g_avg}")
    print(f"Average Red Intensity: {r_avg}")

    cv2.imshow("Resized Image", resized)
    cv2.imshow("Blue Channel", B)
    cv2.imshow("Green Channel", G)
    cv2.imshow("Red Channel", R)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def transformation_pipeline():
    if image is None:
        print("No image loaded yet. Please use Option 1 first.")
        return

    try:
        angle = float(input("Enter rotation angle in degrees: "))
    except ValueError:
        print("Invalid angle entered.")
        return

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    scale = 1.0

    # Step 1: Rotate
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    cv2.imshow("Step 1 - Rotated", rotated)

    # Step 2: Crop central 60%
    rh, rw = rotated.shape[:2]
    margin_h = int(rh * 0.2)   # 20% off top and bottom
    margin_w = int(rw * 0.2)   # 20% off left and right
    cropped = rotated[margin_h: rh - margin_h, margin_w: rw - margin_w]
    cv2.imshow("Step 2 - Cropped (Central 60%)", cropped)

    # Step 3: Flip horizontally
    flipped = cv2.flip(cropped, 1)
    cv2.imshow("Step 3 - Flipped", flipped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def edge_quality_scan():
    if image is None:
        print("No image loaded yet. Please use Option 1 first.")
        return

    blurred = cv2.GaussianBlur(image, (5, 5), sigmaX=0)
    edges = cv2.Canny(blurred, 50, 150)

    cv2.imshow("Edge Map", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    edge_pixel_count = cv2.countNonZero(edges)
    print(f"Total edge pixels: {edge_pixel_count}")

    if edge_pixel_count > 5000:
        print("Verdict: High texture (good detail)")
    else:
        print("Verdict: Low texture (may need re-shoot)")


def show_menu():
    print("\n===== Food Delivery Image Quality Inspector =====")
    print("1. Load & inspect image")
    print("2. Resize and analyse colour channels")
    print("3. Apply transformation pipeline")
    print("4. Run edge-based quality scan")
    print("5. Exit")


def main():
    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            load_and_inspect()
        elif choice == "2":
            resize_and_analyse()
        elif choice == "3":
            transformation_pipeline()
        elif choice == "4":
            edge_quality_scan()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please select a number between 1 and 5.")


if __name__ == "__main__":
    main()