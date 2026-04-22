import os
import re

folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\HR\hr_analytics"

files = [f for f in os.listdir(folder) if f.lower().endswith('.jpeg') or f.lower().endswith('.jpg')]

def extract_time(filename):
    # Extract HHMMSS from Screenshot_22-4-2026_HHMMSS_alison.com.jpeg
    match = re.search(r'_(\d+)_alison', filename)
    return match.group(1).zfill(10) if match else filename

files.sort(key=extract_time)

print(f"Found {len(files)} files. Renaming...\n")
for i, old_name in enumerate(files, start=1):
    new_name = f"hr_analytics_slide_{i:03d}.jpeg"
    old_path = os.path.join(folder, old_name)
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)
    print(f"  {old_name} -> {new_name}")

print(f"\nDone. Renamed {len(files)} files.")
