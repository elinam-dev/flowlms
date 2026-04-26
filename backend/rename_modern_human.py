import os

folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\HR\modern_human"

files = sorted([f for f in os.listdir(folder) if f.endswith('.jpeg')])
print(f"Found {len(files)} files")

for i, filename in enumerate(files, start=1):
    new_name = f"modern_human_slide_{i:03d}.jpeg"
    os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
    print(f"{filename} -> {new_name}")

print("Done!")
