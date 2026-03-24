import os

folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\HR\introduction_to_modern_human_resource_management"
screenshots = sorted([f for f in os.listdir(folder) if f.startswith('Screenshot')])
for i, f in enumerate(screenshots, start=1):
    os.rename(os.path.join(folder, f), os.path.join(folder, f'introduction_to_modern_hrm{i}.jpeg'))
print(f'Renamed {len(screenshots)} files')
