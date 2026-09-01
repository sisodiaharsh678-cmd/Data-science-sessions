"""
Reduces the full 140k dataset down to a smaller subset for fast training.

STEP 1: Edit the SOURCE_DIR line below to match YOUR extracted folder path.
STEP 2: Save this file.
STEP 3: Run it: python make_subset.py
"""

import os
import random
import shutil

# ============================================
# EDIT THIS LINE ONLY — paste your real path here
# ============================================
SOURCE_DIR = "/Users/harshsisodiya678/Downloads/archive/real_vs_fake"

# Where the smaller subset will be copied to (inside your project)
DEST_DIR = "data"

# How many images per class per split
SUBSET_SIZES = {
    "train": 4000,
    "valid": 500,
    "test": 500,
}

CLASSES = ["real", "fake"]
SPLITS = ["train", "valid", "test"]


def copy_subset():
    if not os.path.isdir(SOURCE_DIR):
        print(f"ERROR: This folder does not exist: {SOURCE_DIR}")
        print("Fix the SOURCE_DIR line at the top of this file, then run again.")
        return

    for split in SPLITS:
        for cls in CLASSES:
            src_folder = os.path.join(SOURCE_DIR, split, cls)
            dst_folder = os.path.join(DEST_DIR, split, cls)

            if not os.path.isdir(src_folder):
                print(f"WARNING: not found, skipping: {src_folder}")
                continue

            os.makedirs(dst_folder, exist_ok=True)

            all_images = [f for f in os.listdir(src_folder)
                          if f.lower().endswith((".jpg", ".jpeg", ".png"))]

            n = min(SUBSET_SIZES[split], len(all_images))
            chosen = random.sample(all_images, n)

            for fname in chosen:
                shutil.copy2(os.path.join(src_folder, fname), os.path.join(dst_folder, fname))

            print(f"{split}/{cls}: copied {n} images")

    print("\nDone! Now run: python check_data.py")


if __name__ == "__main__":
    copy_subset()
