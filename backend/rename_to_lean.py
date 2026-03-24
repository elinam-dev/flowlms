import os
from pathlib import Path

folder = Path(__file__).parent / "uploads" / "images" / "supply_chain" / "lean_sigma_six"
files = sorted([f for f in folder.glob("learn_sigma_six*.jpeg")])

for file in files:
    num = file.name.replace("learn_sigma_six", "").replace(".jpeg", "")
    new_name = folder / f"lean_sigma_six{num}.jpeg"
    file.rename(new_name)
    print(f"Renamed: {file.name} -> {new_name.name}")

print(f"\nRenamed {len(files)} files")
