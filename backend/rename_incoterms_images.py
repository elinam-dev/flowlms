import os

incoterms_folder = "uploads/images/incoterms"

# Get all image files
files = [f for f in os.listdir(incoterms_folder) if f.endswith(('.jpeg', '.jpg', '.png'))]
files.sort()

print(f"Found {len(files)} images")

# Rename files sequentially
for i, old_name in enumerate(files, 1):
    old_path = os.path.join(incoterms_folder, old_name)
    new_name = f"incoterms{i}.jpeg"
    new_path = os.path.join(incoterms_folder, new_name)
    
    os.rename(old_path, new_path)
    print(f"Renamed: {old_name} -> {new_name}")

print(f"\nRenamed {len(files)} images successfully")
