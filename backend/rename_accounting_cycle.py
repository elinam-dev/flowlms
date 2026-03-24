import os
from pathlib import Path

folder = Path(__file__).parent / "uploads" / "images" / "Finance" / "the_accounting_cycle"
files = sorted([f for f in folder.glob("*.jpeg")])

for i, file in enumerate(files, 1):
    new_name = folder / f"the_accounting_cycle{i}.jpeg"
    file.rename(new_name)
    print(f"Renamed: {file.name} -> {new_name.name}")

print(f"\nRenamed {len(files)} files")
