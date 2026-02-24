import os

folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\B2B"
files = sorted([f for f in os.listdir(folder) if f.endswith('.jpeg')])

for i, file in enumerate(files, 1):
    old_path = os.path.join(folder, file)
    new_path = os.path.join(folder, f"B2B{i}.jpeg")
    os.rename(old_path, new_path)
    print(f"Renamed {file} -> B2B{i}.jpeg")

print(f"\nRenamed {len(files)} files")
