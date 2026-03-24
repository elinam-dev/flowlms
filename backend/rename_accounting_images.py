#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT_DIR = Path(__file__).parent
images_dir = ROOT_DIR / "uploads" / "images" / "Finance" / "fundamentals_of_accounting"

# Get all image files
image_files = sorted([f for f in images_dir.glob("*.*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])

print(f"Found {len(image_files)} images")

# Rename files
for i, old_file in enumerate(image_files, start=1):
    new_name = f"fundamentals_of_accounting{i}.jpeg"
    new_path = images_dir / new_name
    
    if old_file.name != new_name:
        shutil.move(str(old_file), str(new_path))
        print(f"Renamed: {old_file.name} -> {new_name}")

print(f"\nDone! Renamed {len(image_files)} files")
