#!/usr/bin/env python3
"""
Rename diploma_in_strategic images to diploma_in_strategic_001.jpeg etc.
"""
from pathlib import Path

IMG_DIR = Path(__file__).parent / "uploads" / "images" / "HR" / "diploma_in_strategic"

files = sorted([f for f in IMG_DIR.iterdir() if f.suffix.lower() in ['.jpeg', '.jpg']])
print(f"Found {len(files)} images, renaming...")

for i, f in enumerate(files, 1):
    new_name = f"diploma_in_strategic_{i:03d}.jpeg"
    new_path = IMG_DIR / new_name
    if f.name != new_name:
        f.rename(new_path)
    print(f"  {f.name} -> {new_name}")

print(f"\nDone! Renamed {len(files)} images.")
