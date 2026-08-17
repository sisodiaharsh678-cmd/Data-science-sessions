"""
Verifies your reduced dataset copied correctly.
Run: python check_data.py
"""

import os

for split in ["train", "valid", "test"]:
    for cls in ["real", "fake"]:
        path = f"data/{split}/{cls}"
        if os.path.isdir(path):
            count = len([f for f in os.listdir(path) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
            print(f"{path} -> {count} images")
        else:
            print(f"{path} -> MISSING")
