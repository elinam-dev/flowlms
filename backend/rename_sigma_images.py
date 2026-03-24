import os
from pathlib import Path

folder = Path(__file__).parent / "uploads" / "images" / "learn_sigma_six"
files = sorted([f for f in folder.glob("*.jpeg")])

for i, file in enumerate(files, 1):
    new_name = folder / f"learn_sigma_six{i}.jpeg"
    file.rename(new_name)
    print(f"Renamed: {file.name} -> {new_name.name}")

print(f"\nRenamed {len(files)} files")
